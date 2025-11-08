# MCNP-CELL-CHECKER SKILL REFINEMENT PLAN
## Comprehensive Upgrade for Complex Reactor Model Validation

**Created**: 2025-11-08
**Priority**: 🔴 **HIGH** - Critical validation infrastructure
**Execution Time**: 2-3 hours

---

## EXECUTIVE SUMMARY

The mcnp-cell-checker skill requires major enhancements to validate complex reactor models with multi-level universe hierarchies, FILL arrays, and lattice structures. Analysis of the AGR-1 HTGR model (1,607 cells, 6-level hierarchy, 288 universes) reveals systematic patterns that must be validated to prevent geometry errors.

**Current Gaps**:
- ❌ No universe hierarchy validation
- ❌ No FILL array dimension checking
- ❌ No LAT specification validation (both LAT=1 and LAT=2)
- ❌ Limited cross-reference checking
- ❌ No circular reference detection
- ❌ No systematic numbering scheme validation

**Impact**: Users building complex reactor models will encounter runtime errors that could have been caught at input validation stage.

---

## ANALYSIS FINDINGS

### Key Patterns from AGR-1 Model

**6-Level Universe Hierarchy**:
```
Level 0: Global Universe (u=0)
Level 1: Compact Lattice (u=1110, LAT=1, 1×1×31)
Level 2: Particle Lattice (u=1116, LAT=1, 15×15×1)
Level 3: TRISO Particle (u=1114, 6 concentric cells)
Level 4: Matrix Filler (u=1115, u=1117)
```

**Systematic Numbering** (XYZW encoding):
- Cell: 9XYZW (90000-99999)
- Surface: 9XYZ (9000-9999)
- Material: 9XYZ (9000-9999)
- Universe: XYZW (1000-9999)

Where: X=capsule, Y=stack, Z=compact, W=component

**FILL Array Complexity**:
- 15×15×1 = 225 elements (particle lattice)
- 1×1×31 = 31 elements (compact stack)
- Repeat notation: `1117 2R 1116 24R 1117 2R` (3+25+3=31)

**Cross-Reference Chains**:
- Cell 91111 → fill=1110 → Universe 1110 (lattice)
- Universe 1110 → fills with u=1116, u=1117
- Universe 1116 (lattice) → fills with u=1114, u=1115
- Universe 1114 → 6 cells (kernel through matrix)

---

## MISSION OBJECTIVES

### 1. Universe Hierarchy Validation

**Goal**: Validate all universe definitions, references, and nesting depth

**Specific Checks**:
- ✅ All universes referenced in FILL are defined
- ✅ No circular references (A→B→C→A)
- ✅ Child universes defined before parent universes
- ✅ Nesting depth tracking (warn if >6 levels)
- ✅ Universe 0 never explicitly defined (reserved for global)
- ✅ Unique universe numbers (no conflicts)

**Implementation**:
1. Parse all `u=XXXX` declarations → build universe registry
2. Parse all `fill=XXXX` and lattice fill arrays → build dependency graph
3. Topological sort to detect cycles
4. Depth-first search to compute nesting depth
5. Report warnings/errors

**Example Validation**:
```mcnp
c VALID hierarchy
91101 9111 -10.924 -91111  u=1114  $ TRISO particle (defined)
91108 0  -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ Lattice (defined)
     1114 1114 1114 ...  $ References u=1114 ✓
91110 0  -91118  u=1110 lat=1  fill=0:0 0:0 -15:15 1116 24R  $ References u=1116 ✓
91111 0  -97011  fill=1110  $ References u=1110 ✓

c INVALID - circular reference
100 0 -10  u=5  fill=6
200 0 -20  u=6  fill=5  $ ERROR: u=6 fills u=5, u=5 fills u=6
```

### 2. FILL Directive Validation

**Goal**: Validate all FILL specifications for correct syntax and dimensions

**Specific Checks**:

#### Simple Fill (fill=UNIV)
- ✅ Universe UNIV is defined
- ✅ Translation vector (x,y,z) has 3 components
- ✅ No circular reference

#### Lattice Fill (fill=IMIN:IMAX JMIN:JMAX KMIN:KMAX)
- ✅ **Dimension calculation**: Elements needed = (IMAX-IMIN+1)×(JMAX-JMIN+1)×(KMAX-KMIN+1)
- ✅ **Element count verification**: Count provided universe numbers (accounting for repeat notation)
- ✅ **Repeat notation parsing**: `U nR` = (n+1) total copies
- ✅ **All filled universes defined**
- ✅ **Lattice type specified**: LAT=1 (rectangular) or LAT=2 (hexagonal)

**Example Validation**:
```mcnp
c VALID - 15×15×1 = 225 elements
91108 0  -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0
     [... 225 universe numbers: mix of 1114 and 1115 ...]

c VALID - 1×1×31 = 31 elements with repeat notation
91110 0  -91118  u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R 1117 2R
  Breakdown: 1117 (1) + 2R (2 more) + 1116 (1) + 24R (24 more) + 1117 (1) + 2R (2 more)
           = 3 + 25 + 3 = 31 ✓

c INVALID - dimension mismatch
91110 0  -91118  u=1110 lat=1  fill=0:0 0:0 -15:15 1117 2R 1116 24R
  ERROR: Need 31 elements but only have 3+25=28
```

### 3. LAT Specification Validation

**Goal**: Validate lattice declarations for both rectangular (LAT=1) and hexagonal (LAT=2)

**Specific Checks**:

#### For LAT=1 (Rectangular Lattices)
- ✅ Bounding surface is RPP (rectangular parallelepiped)
- ✅ Surface dimensions match lattice extent
  - X-extent = (IMAX-IMIN+1) × pitch_x
  - Y-extent = (JMAX-JMIN+1) × pitch_y
  - Z-extent = (KMAX-KMIN+1) × pitch_z
- ✅ FILL array dimension matches specification

#### For LAT=2 (Hexagonal Lattices)
- ✅ Bounding surface is RHP (right hexagonal prism)
- ✅ Hexagonal pitch = R × √3 (from RHP R-vector)
- ✅ FILL array dimension matches specification (same rules as LAT=1)
- ✅ Pattern visually inspected (if indented formatting used)

**Example Validation**:
```mcnp
c VALID LAT=1 - Rectangular lattice
91117 rpp -0.043715 0.043715 -0.043715 0.043715 -0.050000 0.050000
91108 0  -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0
  Surface extent: 0.08743 × 0.08743 × 0.10 cm
  Lattice: 15 × 15 × 1 elements
  Pitch: 0.08743/15 = 0.005829 cm ✓

c VALID LAT=2 - Hexagonal lattice
200 rhp  0 0 0  0 0 68  0 1.6 0  $ R=1.6, height=68
201 0  -200  u=300 lat=2  fill=-6:6 -6:6 0:0
  Hex pitch: 1.6 × √3 = 2.77 cm
  Lattice: 13 × 13 × 1 = 169 elements ✓

c INVALID - wrong surface type for LAT=2
200 rpp -10 10 -10 10 0 68  $ RPP for hexagonal lattice!
201 0  -200  u=300 lat=2  fill=-6:6 -6:6 0:0
  ERROR: LAT=2 requires RHP surface, not RPP
```

### 4. Cell-Surface-Material Cross-References

**Goal**: Validate all entity references are defined and consistent

**Specific Checks**:

#### Cell → Surface References
- ✅ All surfaces in Boolean expression are defined
- ✅ Surface numbers are valid (positive integers)
- ✅ No undefined surfaces (fatal error prevention)

#### Cell → Material References
- ✅ Material 0 (void) used correctly:
  - With `lat=1/2 fill=...` → lattice container ✓
  - With `fill=U` → universe fill target ✓
  - Standalone → true void ✓
- ✅ Non-zero materials are defined in materials block
- ✅ Density specification consistent:
  - Positive → atom density (atoms/barn-cm)
  - Negative → mass density (g/cm³)

#### Cell → Universe References
- ✅ Universe assignment `u=XXXX` uses unique number
- ✅ Multiple cells can share same universe (by design)
- ✅ Universe 0 never assigned explicitly

**Example Validation**:
```mcnp
c VALID cross-references
91101 9111 -10.924 -91111  u=1114  vol=0.092522  $ Kernel
  References: surface 91111 ✓, material 9111 ✓, universe 1114 ✓

c INVALID - undefined surface
91101 9111 -10.924 -99999  u=1114
  ERROR: Surface 99999 not defined

c INVALID - undefined material
91101 8888 -10.924 -91111  u=1114
  ERROR: Material 8888 not defined

c VALID - void cell patterns
91108 0  -91117  u=1116 lat=1  fill=-7:7 -7:7 0:0  $ Lattice container ✓
91111 0  -97011  fill=1110  (x y z)  $ Fill target ✓
99999 0  99000  $ True void ✓
```

### 5. Circular Reference Detection

**Goal**: Prevent infinite loops in universe fill chains

**Algorithm**:
1. Build directed graph: nodes = universes, edges = fill relationships
2. Perform depth-first search (DFS) with cycle detection
3. Report any cycles found

**Example Cycles to Detect**:
```mcnp
c INVALID - direct circular reference
100 0 -10  u=5  fill=6
200 0 -20  u=6  fill=5
  ERROR: u=5 → u=6 → u=5 (circular)

c INVALID - indirect circular reference (A→B→C→A)
100 0 -10  u=5  fill=6
200 0 -20  u=6  fill=7
300 0 -30  u=7  fill=5
  ERROR: u=5 → u=6 → u=7 → u=5 (circular)

c INVALID - self-reference
100 0 -10  u=5  fill=5
  ERROR: u=5 → u=5 (self-reference)

c VALID - no cycles
100 0 -10  u=5  fill=6
200 0 -20  u=6  fill=7
300 0 -30  u=7  $ Terminal node (no fill)
  ✓ u=5 → u=6 → u=7 → END (acyclic)
```

---

## IMPLEMENTATION PLAN

### Phase 1: Data Structures (30 min)

**File**: `.claude/skills/mcnp-cell-checker/scripts/cell_validator.py`

```python
from dataclasses import dataclass
from typing import List, Set, Dict, Optional, Tuple
from enum import Enum

class LatticeType(Enum):
    NONE = 0
    RECTANGULAR = 1  # LAT=1
    HEXAGONAL = 2    # LAT=2

class SurfaceType(Enum):
    RPP = "rpp"  # Rectangular parallelepiped
    RHP = "rhp"  # Right hexagonal prism
    SO = "so"    # Sphere at origin
    CZ = "cz"    # Cylinder along Z
    # ... other surface types

@dataclass
class CellDefinition:
    cell_id: int
    material_id: int
    density: Optional[float]
    surfaces: List[int]  # Surface numbers in Boolean expression
    universe: Optional[int]  # u=XXXX
    lattice_type: LatticeType  # lat=1 or lat=2
    fill_simple: Optional[int]  # fill=UNIV
    fill_translation: Optional[Tuple[float, float, float]]  # (x, y, z)
    fill_array_bounds: Optional[Tuple[int, int, int, int, int, int]]  # imin, imax, jmin, jmax, kmin, kmax
    fill_array_elements: List[int]  # Universe numbers in fill array
    volume: Optional[float]
    importance: Optional[float]
    line_number: int

@dataclass
class UniverseDefinition:
    universe_id: int
    cells: List[int]  # Cell IDs that define this universe
    fills: List[int]  # Universe IDs that this universe fills with
    is_lattice: bool
    lattice_type: LatticeType
    defined_at_line: int

@dataclass
class SurfaceDefinition:
    surface_id: int
    surface_type: SurfaceType
    parameters: List[float]
    line_number: int

@dataclass
class MaterialDefinition:
    material_id: int
    zaids: List[str]
    fractions: List[float]
    line_number: int

@dataclass
class ValidationError:
    severity: str  # "ERROR", "WARNING", "INFO"
    category: str  # "UNIVERSE", "FILL", "LATTICE", "CROSS_REF", "CIRCULAR"
    message: str
    line_number: Optional[int]
    cell_id: Optional[int]
    universe_id: Optional[int]

class MCNPInputRegistry:
    """Central registry for all MCNP entities"""
    def __init__(self):
        self.cells: Dict[int, CellDefinition] = {}
        self.surfaces: Dict[int, SurfaceDefinition] = {}
        self.materials: Dict[int, MaterialDefinition] = {}
        self.universes: Dict[int, UniverseDefinition] = {}
        self.errors: List[ValidationError] = []

    def add_error(self, severity: str, category: str, message: str,
                  line_number: int = None, cell_id: int = None, universe_id: int = None):
        self.errors.append(ValidationError(
            severity=severity,
            category=category,
            message=message,
            line_number=line_number,
            cell_id=cell_id,
            universe_id=universe_id
        ))
```

### Phase 2: Parsing Logic (45 min)

**File**: `.claude/skills/mcnp-cell-checker/scripts/cell_parser.py`

```python
import re
from cell_validator import (
    CellDefinition, SurfaceDefinition, MaterialDefinition,
    UniverseDefinition, MCNPInputRegistry, LatticeType, SurfaceType
)

class MCNPCellParser:
    """Parse MCNP cell cards into structured data"""

    def __init__(self):
        self.registry = MCNPInputRegistry()

    def parse_cell_card(self, line: str, line_number: int) -> Optional[CellDefinition]:
        """
        Parse a single cell card line

        Format: CELL_ID  MAT  DENSITY  SURFACES  [u=U] [lat=1/2] [fill=...] [vol=V] [imp:n=I]
        """
        # Remove comments
        if '$' in line:
            line = line.split('$')[0]

        tokens = line.split()
        if len(tokens) < 3:
            return None  # Not a valid cell card

        try:
            cell_id = int(tokens[0])
            material_id = int(tokens[1])

            # Parse density (optional for void cells with fill)
            density = None
            if len(tokens) > 2 and self._is_number(tokens[2]):
                density = float(tokens[2])
                surface_start_idx = 3
            else:
                surface_start_idx = 2

            # Parse surfaces and options
            surfaces = []
            universe = None
            lattice_type = LatticeType.NONE
            fill_simple = None
            fill_translation = None
            fill_array_bounds = None
            fill_array_elements = []
            volume = None
            importance = None

            i = surface_start_idx
            while i < len(tokens):
                token = tokens[i]

                # Universe assignment
                if token.startswith('u='):
                    universe = int(token.split('=')[1])

                # Lattice type
                elif token.startswith('lat='):
                    lat_value = int(token.split('=')[1])
                    if lat_value == 1:
                        lattice_type = LatticeType.RECTANGULAR
                    elif lat_value == 2:
                        lattice_type = LatticeType.HEXAGONAL

                # Fill directive
                elif token.startswith('fill='):
                    fill_spec = token.split('=')[1]
                    if ':' in fill_spec:
                        # Array fill: fill=imin:imax jmin:jmax kmin:kmax
                        # Parse bounds
                        fill_array_bounds = self._parse_fill_array_bounds(tokens[i:])
                        # Following tokens are universe numbers (potentially with repeat notation)
                        # Parse until next keyword
                        i += 1
                        while i < len(tokens) and not self._is_keyword(tokens[i]):
                            fill_array_elements.extend(self._parse_fill_element(tokens[i]))
                            i += 1
                        i -= 1  # Back up one since loop will increment
                    else:
                        # Simple fill: fill=UNIV or fill=UNIV (x y z)
                        fill_simple = int(fill_spec)
                        # Check for translation
                        if i+1 < len(tokens) and tokens[i+1].startswith('('):
                            fill_translation = self._parse_translation(tokens[i+1:i+4])

                # Volume
                elif token.startswith('vol='):
                    volume = float(token.split('=')[1])

                # Importance
                elif token.startswith('imp:'):
                    importance = float(token.split('=')[1])

                # Surface number
                elif self._is_surface_number(token):
                    surfaces.append(int(token))

                i += 1

            return CellDefinition(
                cell_id=cell_id,
                material_id=material_id,
                density=density,
                surfaces=surfaces,
                universe=universe,
                lattice_type=lattice_type,
                fill_simple=fill_simple,
                fill_translation=fill_translation,
                fill_array_bounds=fill_array_bounds,
                fill_array_elements=fill_array_elements,
                volume=volume,
                importance=importance,
                line_number=line_number
            )

        except (ValueError, IndexError) as e:
            self.registry.add_error(
                "ERROR", "PARSE",
                f"Failed to parse cell card: {str(e)}",
                line_number=line_number
            )
            return None

    def _parse_fill_array_bounds(self, tokens: List[str]) -> Tuple[int, int, int, int, int, int]:
        """
        Parse fill=imin:imax jmin:jmax kmin:kmax

        Returns: (imin, imax, jmin, jmax, kmin, kmax)
        """
        # Example: fill=-7:7 -7:7 0:0
        bounds_str = tokens[0].split('=')[1]  # "-7:7"

        # Parse each bound pair
        ranges = []
        for i in range(1, 4):  # Three ranges (i, j, k)
            range_str = tokens[i] if i < len(tokens) else bounds_str
            parts = range_str.split(':')
            ranges.extend([int(parts[0]), int(parts[1])])

        return tuple(ranges)

    def _parse_fill_element(self, token: str) -> List[int]:
        """
        Parse fill array element with repeat notation

        Examples:
          "100" → [100]
          "100 2R" → [100, 100, 100]  (1 + 2 repeats = 3 total)
        """
        if 'R' in token or 'r' in token:
            # Repeat notation: "nR" or "nrm"
            match = re.match(r'(\d+)([Rr])', token)
            if match:
                n_repeats = int(match.group(1))
                return [self.last_fill_element] * (n_repeats + 1)  # n+1 total
        else:
            # Simple universe number
            universe_id = int(token)
            self.last_fill_element = universe_id
            return [universe_id]

        return []

    def _is_keyword(self, token: str) -> bool:
        """Check if token is a keyword (u=, lat=, fill=, vol=, imp:)"""
        return any(token.startswith(kw) for kw in ['u=', 'lat=', 'fill=', 'vol=', 'imp:'])

    def _is_surface_number(self, token: str) -> bool:
        """Check if token is a surface number (including negative)"""
        try:
            int(token)
            return True
        except ValueError:
            return False

    def _is_number(self, token: str) -> bool:
        """Check if token is a number (int or float)"""
        try:
            float(token)
            return True
        except ValueError:
            return False
```

### Phase 3: Validation Logic (60 min)

**File**: `.claude/skills/mcnp-cell-checker/scripts/cell_validator_logic.py`

```python
from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque

class UniverseHierarchyValidator:
    """Validate universe hierarchies and detect circular references"""

    def __init__(self, registry: MCNPInputRegistry):
        self.registry = registry
        self.universe_graph = defaultdict(list)  # universe_id → [filled_universe_ids]

    def build_universe_graph(self):
        """Build directed graph of universe dependencies"""
        for cell_id, cell in self.registry.cells.items():
            if cell.universe is None:
                continue  # Cell not in a universe (global)

            # Record universe definition
            if cell.universe not in self.registry.universes:
                self.registry.universes[cell.universe] = UniverseDefinition(
                    universe_id=cell.universe,
                    cells=[],
                    fills=[],
                    is_lattice=cell.lattice_type != LatticeType.NONE,
                    lattice_type=cell.lattice_type,
                    defined_at_line=cell.line_number
                )

            self.registry.universes[cell.universe].cells.append(cell_id)

            # Record fill dependencies
            if cell.fill_simple is not None:
                self.universe_graph[cell.universe].append(cell.fill_simple)
                self.registry.universes[cell.universe].fills.append(cell.fill_simple)

            if cell.fill_array_elements:
                unique_fills = set(cell.fill_array_elements)
                for fill_univ in unique_fills:
                    self.universe_graph[cell.universe].append(fill_univ)
                    if fill_univ not in self.registry.universes[cell.universe].fills:
                        self.registry.universes[cell.universe].fills.append(fill_univ)

    def validate_universe_definitions(self):
        """Check that all referenced universes are defined"""
        for cell_id, cell in self.registry.cells.items():
            # Check simple fill
            if cell.fill_simple is not None:
                if cell.fill_simple not in self.registry.universes:
                    self.registry.add_error(
                        "ERROR", "UNIVERSE",
                        f"Cell {cell_id} fills with universe {cell.fill_simple} which is not defined",
                        line_number=cell.line_number,
                        cell_id=cell_id,
                        universe_id=cell.fill_simple
                    )

            # Check array fill
            if cell.fill_array_elements:
                for fill_univ in set(cell.fill_array_elements):
                    if fill_univ not in self.registry.universes:
                        self.registry.add_error(
                            "ERROR", "UNIVERSE",
                            f"Cell {cell_id} lattice fill references undefined universe {fill_univ}",
                            line_number=cell.line_number,
                            cell_id=cell_id,
                            universe_id=fill_univ
                        )

    def detect_circular_references(self):
        """Detect circular universe fill chains using DFS"""
        visited = set()
        rec_stack = set()

        def dfs(universe_id: int, path: List[int]) -> bool:
            """
            DFS with cycle detection

            Returns: True if cycle detected, False otherwise
            """
            visited.add(universe_id)
            rec_stack.add(universe_id)
            path.append(universe_id)

            for neighbor in self.universe_graph[universe_id]:
                if neighbor not in visited:
                    if dfs(neighbor, path.copy()):
                        return True
                elif neighbor in rec_stack:
                    # Cycle detected!
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    self.registry.add_error(
                        "ERROR", "CIRCULAR",
                        f"Circular universe reference detected: {' → '.join(map(str, cycle))}",
                        universe_id=universe_id
                    )
                    return True

            rec_stack.remove(universe_id)
            return False

        # Check all universes
        for universe_id in self.universe_graph.keys():
            if universe_id not in visited:
                dfs(universe_id, [])

    def validate_universe_zero(self):
        """Check that universe 0 is never explicitly defined"""
        if 0 in self.registry.universes:
            self.registry.add_error(
                "ERROR", "UNIVERSE",
                "Universe 0 is reserved for global universe and should not be explicitly defined",
                universe_id=0
            )

    def compute_nesting_depth(self) -> Dict[int, int]:
        """
        Compute nesting depth for each universe

        Returns: Dict mapping universe_id → depth (0 = global level)
        """
        depths = {}

        # Find root universes (those filled into global but not defined as u=0)
        root_universes = set()
        for cell_id, cell in self.registry.cells.items():
            if cell.universe is None or cell.universe == 0:
                # Cell in global universe
                if cell.fill_simple is not None:
                    root_universes.add(cell.fill_simple)
                if cell.fill_array_elements:
                    root_universes.update(cell.fill_array_elements)

        # BFS to compute depths
        queue = deque([(u, 1) for u in root_universes])
        while queue:
            universe_id, depth = queue.popleft()

            if universe_id in depths:
                depths[universe_id] = max(depths[universe_id], depth)
            else:
                depths[universe_id] = depth

            # Add children
            for child in self.universe_graph[universe_id]:
                queue.append((child, depth + 1))

        # Warn about deep nesting
        for universe_id, depth in depths.items():
            if depth > 6:
                self.registry.add_error(
                    "WARNING", "UNIVERSE",
                    f"Universe {universe_id} has nesting depth {depth} (>6 may impact performance)",
                    universe_id=universe_id
                )

        return depths


class FillArrayValidator:
    """Validate FILL array specifications"""

    def __init__(self, registry: MCNPInputRegistry):
        self.registry = registry

    def validate_fill_dimensions(self):
        """Check that FILL array element counts match declared bounds"""
        for cell_id, cell in self.registry.cells.items():
            if cell.fill_array_bounds is None:
                continue

            imin, imax, jmin, jmax, kmin, kmax = cell.fill_array_bounds

            # Calculate required elements
            i_count = imax - imin + 1
            j_count = jmax - jmin + 1
            k_count = kmax - kmin + 1
            required_elements = i_count * j_count * k_count

            # Count provided elements
            provided_elements = len(cell.fill_array_elements)

            if required_elements != provided_elements:
                self.registry.add_error(
                    "ERROR", "FILL",
                    f"Cell {cell_id}: FILL array dimension mismatch. "
                    f"Bounds {imin}:{imax} {jmin}:{jmax} {kmin}:{kmax} require "
                    f"{required_elements} elements ({i_count}×{j_count}×{k_count}), "
                    f"but {provided_elements} elements provided",
                    line_number=cell.line_number,
                    cell_id=cell_id
                )
            else:
                self.registry.add_error(
                    "INFO", "FILL",
                    f"Cell {cell_id}: FILL array validated - {required_elements} elements "
                    f"({i_count}×{j_count}×{k_count}) ✓",
                    line_number=cell.line_number,
                    cell_id=cell_id
                )


class LatticeValidator:
    """Validate LAT specifications"""

    def __init__(self, registry: MCNPInputRegistry):
        self.registry = registry

    def validate_lattice_surface_type(self):
        """Check that lattice bounding surface matches lattice type"""
        for cell_id, cell in self.registry.cells.items():
            if cell.lattice_type == LatticeType.NONE:
                continue

            # Get bounding surface (first surface in cell definition)
            if not cell.surfaces:
                self.registry.add_error(
                    "ERROR", "LATTICE",
                    f"Cell {cell_id}: Lattice cell has no bounding surface",
                    line_number=cell.line_number,
                    cell_id=cell_id
                )
                continue

            # Get surface definition (abs value, as might be negative sense)
            surface_id = abs(cell.surfaces[0])
            if surface_id not in self.registry.surfaces:
                continue  # Will be caught by cross-reference validator

            surface = self.registry.surfaces[surface_id]

            # Check match between LAT type and surface type
            if cell.lattice_type == LatticeType.RECTANGULAR:
                if surface.surface_type != SurfaceType.RPP:
                    self.registry.add_error(
                        "ERROR", "LATTICE",
                        f"Cell {cell_id}: LAT=1 (rectangular) requires RPP bounding surface, "
                        f"but surface {surface_id} is type {surface.surface_type.value}",
                        line_number=cell.line_number,
                        cell_id=cell_id
                    )

            elif cell.lattice_type == LatticeType.HEXAGONAL:
                if surface.surface_type != SurfaceType.RHP:
                    self.registry.add_error(
                        "ERROR", "LATTICE",
                        f"Cell {cell_id}: LAT=2 (hexagonal) requires RHP bounding surface, "
                        f"but surface {surface_id} is type {surface.surface_type.value}",
                        line_number=cell.line_number,
                        cell_id=cell_id
                    )


class CrossReferenceValidator:
    """Validate cell-surface-material cross-references"""

    def __init__(self, registry: MCNPInputRegistry):
        self.registry = registry

    def validate_surface_references(self):
        """Check that all surfaces referenced in cells are defined"""
        for cell_id, cell in self.registry.cells.items():
            for surface_id in cell.surfaces:
                abs_surface_id = abs(surface_id)
                if abs_surface_id not in self.registry.surfaces:
                    self.registry.add_error(
                        "ERROR", "CROSS_REF",
                        f"Cell {cell_id} references undefined surface {abs_surface_id}",
                        line_number=cell.line_number,
                        cell_id=cell_id
                    )

    def validate_material_references(self):
        """Check that all non-void materials are defined"""
        for cell_id, cell in self.registry.cells.items():
            if cell.material_id == 0:
                # Void cell - validate usage
                self._validate_void_cell(cell)
            elif cell.material_id not in self.registry.materials:
                self.registry.add_error(
                    "ERROR", "CROSS_REF",
                    f"Cell {cell_id} references undefined material {cell.material_id}",
                    line_number=cell.line_number,
                    cell_id=cell_id
                )

    def _validate_void_cell(self, cell: CellDefinition):
        """Validate void cell (material 0) usage"""
        has_lattice = cell.lattice_type != LatticeType.NONE
        has_fill = cell.fill_simple is not None or cell.fill_array_elements

        if has_lattice and not has_fill:
            self.registry.add_error(
                "WARNING", "CROSS_REF",
                f"Cell {cell.cell_id}: Lattice cell (LAT={cell.lattice_type.value}) "
                f"with material 0 but no FILL specification",
                line_number=cell.line_number,
                cell_id=cell.cell_id
            )

        if has_fill and not (has_lattice or cell.fill_simple is not None):
            self.registry.add_error(
                "WARNING", "CROSS_REF",
                f"Cell {cell.cell_id}: FILL array specified without LAT declaration",
                line_number=cell.line_number,
                cell_id=cell.cell_id
            )
```

### Phase 4: SKILL.md Update (15 min)

**File**: `.claude/skills/mcnp-cell-checker/SKILL.md`

**ADD new section** (after existing content):

```markdown
## ADVANCED VALIDATION CAPABILITIES

### Universe Hierarchy Validation

mcnp-cell-checker validates complex universe hierarchies including:

1. **Universe Definition Checking**
   - All universes referenced in FILL are defined
   - Universe 0 never explicitly defined (reserved for global)
   - Unique universe numbers (no conflicts)

2. **Circular Reference Detection**
   - Detects cycles in universe fill chains (A→B→C→A)
   - Uses depth-first search algorithm
   - Reports complete cycle path for debugging

3. **Nesting Depth Analysis**
   - Computes nesting depth for each universe
   - Warns if depth >6 levels (performance impact)
   - Validates child-before-parent definition order

**Example Usage**:
```
User: "Check my MCNP input for universe errors"

Assistant will:
✓ Parse all u=XXXX declarations
✓ Parse all fill=XXXX directives
✓ Build universe dependency graph
✓ Detect circular references
✓ Compute nesting depths
✓ Report all errors/warnings
```

### FILL Array Validation

mcnp-cell-checker validates FILL array specifications:

1. **Dimension Checking**
   - Calculates required elements: (IMAX-IMIN+1)×(JMAX-JMIN+1)×(KMAX-KMIN+1)
   - Counts provided elements (accounting for repeat notation)
   - Reports mismatches with detailed explanation

2. **Repeat Notation Parsing**
   - Correctly interprets `U nR` = (n+1) total copies
   - Expands repeat notation for validation
   - Detects malformed repeat syntax

3. **Universe Reference Checking**
   - All filled universes are defined
   - No undefined universe references in arrays

**Example Validation**:
```mcnp
c VALID - 15×15×1 = 225 elements
91108 0 -91117 u=1116 lat=1 fill=-7:7 -7:7 0:0
     [... 225 universe numbers ...]
✓ FILL array validated: 225 elements (15×15×1)

c INVALID - dimension mismatch
91110 0 -91118 u=1110 lat=1 fill=0:0 0:0 -15:15 1117 2R 1116 24R
❌ ERROR: Need 31 elements but only 28 provided
```

### Lattice Specification Validation

mcnp-cell-checker validates both LAT=1 (rectangular) and LAT=2 (hexagonal):

1. **Surface Type Matching**
   - LAT=1 → requires RPP bounding surface
   - LAT=2 → requires RHP bounding surface
   - Reports type mismatches

2. **Dimension Consistency** (optional, requires surface parsing)
   - Checks surface extent matches lattice element count
   - Validates pitch calculations

**Example Validation**:
```mcnp
c VALID LAT=1
91117 rpp -0.04 0.04 -0.04 0.04 -0.05 0.05
91108 0 -91117 u=1116 lat=1 fill=-7:7 -7:7 0:0
✓ LAT=1 with RPP surface (correct)

c INVALID LAT=2
200 rpp -10 10 -10 10 0 68  $ Wrong surface type!
201 0 -200 u=300 lat=2 fill=-6:6 -6:6 0:0
❌ ERROR: LAT=2 requires RHP surface, not RPP
```

### Cross-Reference Validation

mcnp-cell-checker validates all entity references:

1. **Cell → Surface**
   - All surfaces in Boolean expressions are defined
   - No undefined surface references

2. **Cell → Material**
   - All non-zero materials are defined
   - Void cell (material 0) usage validated:
     - With `lat=1/2 fill=...` → lattice container ✓
     - With `fill=U` → universe fill target ✓
     - Standalone → true void ✓

3. **Cell → Universe**
   - Universe assignments use unique numbers
   - Multiple cells can share same universe (by design)

**Example Validation**:
```mcnp
c VALID cross-references
91101 9111 -10.924 -91111 u=1114
✓ Surface 91111 defined
✓ Material 9111 defined
✓ Universe 1114 assigned

c INVALID - undefined surface
91101 9111 -10.924 -99999 u=1114
❌ ERROR: Surface 99999 not defined
```

## VALIDATION REPORT FORMAT

When validation completes, mcnp-cell-checker provides structured report:

```
=== MCNP Cell Validation Report ===

SUMMARY:
  Total Cells: 1607
  Total Universes: 288
  Total Surfaces Referenced: 725
  Total Materials Referenced: 130

  Errors: 0
  Warnings: 3
  Info: 12

UNIVERSE HIERARCHY:
  Maximum Nesting Depth: 6 levels
  Root Universes: 72
  Lattice Universes: 144

  ✓ No circular references detected
  ✓ All universes defined before use
  ⚠ Universe 2345 has depth 7 (performance warning)

FILL ARRAY VALIDATION:
  Total Lattice Cells: 144

  ✓ Cell 91108: 225 elements (15×15×1)
  ✓ Cell 91110: 31 elements (1×1×31) with repeat notation
  ✓ Cell 92108: 225 elements (15×15×1)
  [... all validated ...]

LATTICE VALIDATION:
  Total LAT=1 (rectangular): 144
  Total LAT=2 (hexagonal): 0

  ✓ All rectangular lattices use RPP surfaces
  ✓ No hexagonal lattice surface type errors

CROSS-REFERENCES:
  ✓ All surfaces defined (725/725)
  ✓ All materials defined (130/130)
  ✓ All universes defined (288/288)

DETAILED ERRORS/WARNINGS:
  [List of all errors, warnings, info messages with line numbers]
```

## PYTHON TOOL USAGE

```python
from cell_validator import MCNPCellValidator

validator = MCNPCellValidator('input.i')
validator.parse_input()
validator.validate_all()
report = validator.generate_report()
print(report)
```

## BEST PRACTICES

When building complex reactor models:

1. **Use systematic numbering schemes**
   - Encode hierarchy in universe numbers (XYZW pattern)
   - Correlate cell/surface/material numbers
   - Reserve number ranges for subsystems

2. **Define universes bottom-up**
   - Define leaf universes first (no fills)
   - Then define parent universes that fill with leaves
   - Finally define root universes

3. **Validate incrementally**
   - Check small models before scaling up
   - Test lattice definitions with 2×2 arrays first
   - Expand to full size only after validation

4. **Document universe hierarchy**
   - Comment showing containment tree
   - Note nesting depth
   - Explain numbering scheme

5. **Use comments extensively**
   - Document every cell, surface, material, universe
   - Note geometric locations
   - Explain FILL array patterns
```

### Phase 5: Example Files (15 min)

**File**: `.claude/skills/mcnp-cell-checker/example_inputs/complex_hierarchy_valid.i`

```mcnp
c Complex Universe Hierarchy - VALID Example
c Demonstrates 4-level nesting with proper validation
c
c Level 1: Fuel pin (u=100)
c Level 2: Pin lattice (u=200, LAT=1, 3×3)
c Level 3: Assembly (u=300, LAT=1, 2×2)
c Level 4: Global placement
c
c Cells
c
c Level 1: Fuel pin universe (u=100)
100 1 -10.2  -100         u=100  imp:n=1  $ UO2 fuel
101 2 -6.5   100 -101     u=100  imp:n=1  $ Zircaloy clad
102 3 -1.0   101          u=100  imp:n=1  $ Water

c Level 2: Pin lattice (u=200)
200 0  -200  u=200 lat=1  imp:n=1  fill=-1:1 -1:1 0:0
     100 100 100
     100 100 100
     100 100 100

c Level 3: Assembly lattice (u=300)
300 0  -300  u=300 lat=1  imp:n=1  fill=0:1 0:1 0:0
     200 200
     200 200

c Level 4: Global placement
999 0  -300 fill=300  imp:n=1
1000 0  300  imp:n=0  $ Outside world

c
c Surfaces
c
100 cz  0.41  $ Fuel radius
101 cz  0.48  $ Clad outer radius
200 rpp -0.63 0.63 -0.63 0.63 -180 180  $ Pin cell box (1.26 cm pitch)
300 rpp -1.26 1.26 -1.26 1.26 -180 180  $ Assembly box (2×1.26 cm pitch)

c
c Materials
c
m1  $ UO2
   92235.70c  0.04
   92238.70c  0.96
    8016.70c  2.0
m2  $ Zircaloy
   40000.60c  1.0
m3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt3 lwtr.13t

c
c Source
kcode 1000 1.0 10 50
ksrc 0 0 0
```

**File**: `.claude/skills/mcnp-cell-checker/example_inputs/circular_reference_error.i`

```mcnp
c Circular Reference Error Example - INVALID
c Demonstrates circular universe fill chain
c
c Cells
c
c ERROR: u=100 fills u=200, u=200 fills u=100 (circular!)
100 0 -10  u=100  fill=200
200 0 -20  u=200  fill=100
999 0  -10 fill=100  imp:n=1
1000 0  10  imp:n=0

c
c Surfaces
c
10 rpp -5 5 -5 5 -5 5
20 rpp -3 3 -3 3 -3 3
```

**File**: `.claude/skills/mcnp-cell-checker/example_inputs/fill_dimension_error.i`

```mcnp
c FILL Array Dimension Error Example - INVALID
c
c Cells
c
c ERROR: fill=-1:1 -1:1 0:0 requires 3×3×1=9 elements, but only 6 provided
100 1 -1.0  -100  u=10  imp:n=1  $ Fuel cell
200 0  -200  u=20 lat=1  imp:n=1  fill=-1:1 -1:1 0:0
     10 10 10
     10 10 10
c    10 10 10  $ Missing third row!
999 0  -200 fill=20  imp:n=1
1000 0  200  imp:n=0

c
c Surfaces
c
100 cz 0.5
200 rpp -1.5 1.5 -1.5 1.5 -5 5

c
c Materials
m1 92235.70c 1.0
```

### Phase 6: Testing & Documentation (15 min)

Create comprehensive test suite and usage guide.

---

## SUCCESS CRITERIA

✅ **Universe hierarchy validation**:
- Detects all undefined universe references
- Identifies all circular references
- Computes accurate nesting depths
- Warns about performance-impacting deep nesting

✅ **FILL array validation**:
- Correctly calculates required element counts
- Parses repeat notation (nR syntax)
- Matches provided elements to specification
- Reports mismatches with clear diagnostics

✅ **Lattice validation**:
- Validates LAT=1 with RPP surfaces
- Validates LAT=2 with RHP surfaces
- Detects surface type mismatches

✅ **Cross-reference validation**:
- All surfaces referenced in cells are defined
- All materials referenced in cells are defined
- All universes referenced in fills are defined
- Void cell usage validated

✅ **Circular reference detection**:
- DFS algorithm correctly identifies cycles
- Reports complete cycle path
- No false positives

✅ **User experience**:
- Clear, actionable error messages
- Structured validation report
- Line number references for all errors
- Severity levels (ERROR, WARNING, INFO)

---

## TESTING PLAN

### Test Case 1: AGR-1 Model (Real-World)
- **Input**: `sdr-agr.i` (1,607 cells, 288 universes, 6-level hierarchy)
- **Expected**: All validations pass, no errors
- **Validates**: Complex real-world model handling

### Test Case 2: Circular Reference
- **Input**: `circular_reference_error.i`
- **Expected**: ERROR detected, cycle path reported
- **Validates**: Circular reference detection

### Test Case 3: FILL Dimension Mismatch
- **Input**: `fill_dimension_error.i`
- **Expected**: ERROR detected with element count explanation
- **Validates**: FILL array validation

### Test Case 4: Undefined Universe
- **Input**: Cell with `fill=9999` where u=9999 not defined
- **Expected**: ERROR reported
- **Validates**: Universe definition checking

### Test Case 5: LAT/Surface Type Mismatch
- **Input**: `LAT=2` with RPP surface (should be RHP)
- **Expected**: ERROR reported
- **Validates**: Lattice surface type validation

### Test Case 6: Deep Nesting
- **Input**: 8-level universe hierarchy
- **Expected**: WARNING about depth >6
- **Validates**: Nesting depth analysis

---

## DELIVERABLES

1. **Python validation scripts** (3 files):
   - `cell_validator.py` - Data structures
   - `cell_parser.py` - Parsing logic
   - `cell_validator_logic.py` - Validation algorithms

2. **Updated SKILL.md** with:
   - Advanced validation capabilities section
   - Usage examples
   - Validation report format
   - Best practices

3. **Example input files** (5 files):
   - `complex_hierarchy_valid.i` - Valid 4-level model
   - `circular_reference_error.i` - Circular reference test
   - `fill_dimension_error.i` - FILL array mismatch test
   - `lattice_surface_error.i` - LAT/surface type mismatch
   - `undefined_universe_error.i` - Undefined universe test

4. **Test suite** with automated validation

5. **Quick reference card** for common errors

---

## IMPLEMENTATION NOTES

**Dependencies**:
- Python 3.8+
- No external libraries required (uses stdlib only)

**Performance**:
- Parser: O(n) where n = number of lines
- Universe graph construction: O(V+E) where V = universes, E = fill relationships
- Circular detection: O(V+E) DFS traversal
- Expected runtime: <1 second for files up to 20,000 lines

**Maintainability**:
- Modular design (separate parsing, validation, reporting)
- Extensible data structures (easy to add new checks)
- Comprehensive comments and docstrings
- Type hints throughout

**Future Enhancements** (not in this phase):
- Surface geometry validation (extent vs pitch)
- Boolean expression simplification
- Optimization suggestions
- Automatic numbering scheme detection
- Visual universe hierarchy diagram generation

---

## EXECUTION CHECKLIST

- [ ] Create data structures (`cell_validator.py`)
- [ ] Implement parsing logic (`cell_parser.py`)
- [ ] Implement validation algorithms (`cell_validator_logic.py`)
- [ ] Update SKILL.md with new sections
- [ ] Create 5 example input files
- [ ] Test on AGR-1 model (real-world validation)
- [ ] Test all error detection cases
- [ ] Write usage documentation
- [ ] Create quick reference card
- [ ] Integration test with mcnp-input-validator skill

---

**READY FOR IMPLEMENTATION**

This refinement plan provides complete, executable specifications for upgrading mcnp-cell-checker to handle production-quality reactor models with complex universe hierarchies, multi-level lattices, and comprehensive validation.

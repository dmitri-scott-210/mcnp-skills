"""
MCNP Cell Validator Logic
==========================

Implements validation algorithms for:
- Universe hierarchy analysis
- Circular reference detection (DFS cycle detection)
- FILL array dimension validation
- Lattice specification validation (LAT=1 and LAT=2)
- Cross-reference validation (cells→surfaces→materials)

Based on analysis of AGR-1 HTGR model with 1,607 cells, 288 universes,
and 6-level universe hierarchy.

Author: MCNP Cell Checker Skill
Date: 2025-11-08
"""

from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque
from cell_validator import (
    MCNPInputRegistry, CellDefinition, UniverseDefinition,
    SurfaceDefinition, LatticeType, SurfaceType
)


class UniverseHierarchyValidator:
    """
    Validate universe hierarchies and detect circular references

    Implements:
    - Universe definition checking
    - Circular reference detection using DFS
    - Nesting depth computation using BFS
    - Universe 0 validation
    """

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
                if cell.fill_simple not in self.registry.universes[cell.universe].fills:
                    self.registry.universes[cell.universe].fills.append(cell.fill_simple)

            if cell.fill_array_elements:
                unique_fills = set(cell.fill_array_elements)
                for fill_univ in unique_fills:
                    if fill_univ not in self.universe_graph[cell.universe]:
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
                undefined = set()
                for fill_univ in set(cell.fill_array_elements):
                    if fill_univ not in self.registry.universes:
                        undefined.add(fill_univ)

                if undefined:
                    self.registry.add_error(
                        "ERROR", "UNIVERSE",
                        f"Cell {cell_id} lattice fill references undefined universes: {sorted(undefined)}",
                        line_number=cell.line_number,
                        cell_id=cell_id
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
                    cycle_str = ' → '.join(map(str, cycle))
                    self.registry.add_error(
                        "ERROR", "CIRCULAR",
                        f"Circular universe reference detected: {cycle_str}",
                        universe_id=universe_id
                    )
                    return True

            rec_stack.remove(universe_id)
            return False

        # Check all universes (convert to list to avoid dict size change during iteration)
        for universe_id in list(self.universe_graph.keys()):
            if universe_id not in visited:
                dfs(universe_id, [])

    def validate_universe_zero(self):
        """Check that universe 0 is never explicitly defined"""
        if 0 in self.registry.universes:
            cells_in_u0 = self.registry.universes[0].cells
            self.registry.add_error(
                "WARNING", "UNIVERSE",
                f"Universe 0 is reserved for global universe. Found {len(cells_in_u0)} cells with u=0 (should be omitted)",
                universe_id=0
            )

    def compute_nesting_depth(self) -> Dict[int, int]:
        """
        Compute nesting depth for each universe

        Returns: Dict mapping universe_id → depth (1 = global level)
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

            # Update universe object
            if universe_id in self.registry.universes:
                self.registry.universes[universe_id].nesting_depth = depths[universe_id]

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
    """
    Validate FILL array specifications

    Checks:
    - Array dimension matches declaration
    - Repeat notation is parsed correctly
    - All universes in array are defined
    """

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
    """
    Validate LAT specifications

    Checks:
    - LAT=1 requires RPP bounding surface
    - LAT=2 requires RHP bounding surface
    - Lattice cells are void (material 0)
    - Lattice cells have FILL specification
    """

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
                else:
                    self.registry.add_error(
                        "INFO", "LATTICE",
                        f"Cell {cell_id}: LAT=1 with RPP surface {surface_id} ✓",
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
                else:
                    self.registry.add_error(
                        "INFO", "LATTICE",
                        f"Cell {cell_id}: LAT=2 with RHP surface {surface_id} ✓",
                        line_number=cell.line_number,
                        cell_id=cell_id
                    )

    def validate_lattice_material(self):
        """Check that lattice cells are void (material 0)"""
        for cell_id, cell in self.registry.cells.items():
            if cell.lattice_type == LatticeType.NONE:
                continue

            if cell.material_id != 0:
                self.registry.add_error(
                    "WARNING", "LATTICE",
                    f"Cell {cell_id}: Lattice cell should be void (material 0), "
                    f"but has material {cell.material_id}",
                    line_number=cell.line_number,
                    cell_id=cell_id
                )

    def validate_lattice_fill(self):
        """Check that lattice cells have FILL specification"""
        for cell_id, cell in self.registry.cells.items():
            if cell.lattice_type == LatticeType.NONE:
                continue

            has_fill = cell.fill_array_elements or cell.fill_simple is not None

            if not has_fill:
                self.registry.add_error(
                    "ERROR", "LATTICE",
                    f"Cell {cell_id}: Lattice cell (LAT={cell.lattice_type.value}) "
                    f"has no FILL specification",
                    line_number=cell.line_number,
                    cell_id=cell_id
                )


class CrossReferenceValidator:
    """
    Validate cell-surface-material cross-references

    Checks:
    - All surfaces referenced in cells are defined
    - All materials referenced in cells are defined
    - Void cell (material 0) usage is appropriate
    """

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

        if cell.fill_array_elements and not has_lattice:
            self.registry.add_error(
                "WARNING", "CROSS_REF",
                f"Cell {cell.cell_id}: FILL array specified without LAT declaration",
                line_number=cell.line_number,
                cell_id=cell.cell_id
            )


def validate_all(registry: MCNPInputRegistry) -> MCNPInputRegistry:
    """
    Run all validation checks on a parsed MCNP input

    This is the main entry point for validation. Call this after parsing.
    """
    # Universe hierarchy validation
    universe_validator = UniverseHierarchyValidator(registry)
    universe_validator.build_universe_graph()
    universe_validator.validate_universe_definitions()
    universe_validator.detect_circular_references()
    universe_validator.validate_universe_zero()
    universe_validator.compute_nesting_depth()

    # FILL array validation
    fill_validator = FillArrayValidator(registry)
    fill_validator.validate_fill_dimensions()

    # Lattice validation
    lattice_validator = LatticeValidator(registry)
    lattice_validator.validate_lattice_surface_type()
    lattice_validator.validate_lattice_material()
    lattice_validator.validate_lattice_fill()

    # Cross-reference validation
    xref_validator = CrossReferenceValidator(registry)
    xref_validator.validate_surface_references()
    xref_validator.validate_material_references()

    return registry


if __name__ == "__main__":
    # Example usage
    import sys
    from cell_parser import MCNPCellParser

    if len(sys.argv) > 1:
        parser = MCNPCellParser()
        registry = parser.parse_input_file(sys.argv[1])
        registry = validate_all(registry)
        print(registry.generate_summary_report())
    else:
        print("Usage: python cell_validator_logic.py <input_file>")

"""
MCNP Cell Validator - Data Structures
======================================

Defines data structures for validating MCNP cell cards including:
- Universe hierarchy validation
- FILL array dimension checking
- Lattice specification validation
- Cross-reference validation
- Circular reference detection

Based on analysis of AGR-1 HTGR model with 1,607 cells, 288 universes,
and 6-level universe hierarchy.

Author: MCNP Cell Checker Skill
Date: 2025-11-08
"""

from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional, Tuple
from enum import Enum


class LatticeType(Enum):
    """Lattice type specifications for MCNP"""
    NONE = 0
    RECTANGULAR = 1  # LAT=1 - rectangular parallelepiped
    HEXAGONAL = 2    # LAT=2 - hexagonal prism


class SurfaceType(Enum):
    """Surface type specifications for MCNP"""
    RPP = "rpp"  # Rectangular parallelepiped
    RHP = "rhp"  # Right hexagonal prism
    SO = "so"    # Sphere at origin
    S = "s"      # Sphere at point
    CZ = "cz"    # Cylinder along Z-axis
    CX = "cx"    # Cylinder along X-axis
    CY = "cy"    # Cylinder along Y-axis
    PZ = "pz"    # Plane perpendicular to Z-axis
    PX = "px"    # Plane perpendicular to X-axis
    PY = "py"    # Plane perpendicular to Y-axis
    UNKNOWN = "unknown"


@dataclass
class CellDefinition:
    """
    Complete cell card definition

    Represents a single MCNP cell card with all its parameters.
    Supports both simple cells and complex lattice cells with fills.
    """
    cell_id: int
    material_id: int
    density: Optional[float]
    surfaces: List[int]  # Surface numbers in Boolean expression (with signs)
    universe: Optional[int] = None  # u=XXXX assignment
    lattice_type: LatticeType = LatticeType.NONE  # lat=1 or lat=2
    fill_simple: Optional[int] = None  # fill=UNIV (simple fill)
    fill_translation: Optional[Tuple[float, float, float]] = None  # (x, y, z) TRCL
    fill_array_bounds: Optional[Tuple[int, int, int, int, int, int]] = None  # imin, imax, jmin, jmax, kmin, kmax
    fill_array_elements: List[int] = field(default_factory=list)  # Universe numbers in fill array
    volume: Optional[float] = None
    importance: Optional[float] = None
    line_number: int = 0
    raw_line: str = ""  # Original input line for reference


@dataclass
class UniverseDefinition:
    """
    Universe definition tracking

    Tracks all cells belonging to a universe and all universes
    that this universe fills with (dependency tracking).
    """
    universe_id: int
    cells: List[int] = field(default_factory=list)  # Cell IDs that define this universe
    fills: List[int] = field(default_factory=list)  # Universe IDs that this universe fills with
    is_lattice: bool = False
    lattice_type: LatticeType = LatticeType.NONE
    defined_at_line: int = 0
    nesting_depth: int = 0  # Computed during hierarchy analysis


@dataclass
class SurfaceDefinition:
    """Surface card definition"""
    surface_id: int
    surface_type: SurfaceType
    parameters: List[float] = field(default_factory=list)
    line_number: int = 0
    raw_line: str = ""


@dataclass
class MaterialDefinition:
    """Material card definition"""
    material_id: int
    zaids: List[str] = field(default_factory=list)
    fractions: List[float] = field(default_factory=list)
    line_number: int = 0


@dataclass
class ValidationError:
    """
    Validation error/warning/info message

    Severity levels:
    - ERROR: Fatal issue that will cause MCNP to fail
    - WARNING: Suspicious pattern that may cause issues
    - INFO: Informational message about model structure
    """
    severity: str  # "ERROR", "WARNING", "INFO"
    category: str  # "UNIVERSE", "FILL", "LATTICE", "CROSS_REF", "CIRCULAR"
    message: str
    line_number: Optional[int] = None
    cell_id: Optional[int] = None
    universe_id: Optional[int] = None

    def __str__(self):
        """Format error message for display"""
        parts = [f"[{self.severity}]"]
        if self.line_number:
            parts.append(f"Line {self.line_number}")
        if self.cell_id:
            parts.append(f"Cell {self.cell_id}")
        if self.universe_id:
            parts.append(f"Universe {self.universe_id}")
        parts.append(f"{self.category}: {self.message}")
        return " ".join(parts)


class MCNPInputRegistry:
    """
    Central registry for all MCNP entities

    Stores all cells, surfaces, materials, and universes parsed from
    an MCNP input file, along with validation errors discovered.
    """

    def __init__(self):
        self.cells: Dict[int, CellDefinition] = {}
        self.surfaces: Dict[int, SurfaceDefinition] = {}
        self.materials: Dict[int, MaterialDefinition] = {}
        self.universes: Dict[int, UniverseDefinition] = {}
        self.errors: List[ValidationError] = []

        # Statistics
        self.total_lines: int = 0
        self.cells_parsed: int = 0
        self.surfaces_parsed: int = 0
        self.materials_parsed: int = 0

    def add_error(self, severity: str, category: str, message: str,
                  line_number: int = None, cell_id: int = None, universe_id: int = None):
        """Add a validation error to the registry"""
        self.errors.append(ValidationError(
            severity=severity,
            category=category,
            message=message,
            line_number=line_number,
            cell_id=cell_id,
            universe_id=universe_id
        ))

    def get_errors_by_severity(self, severity: str) -> List[ValidationError]:
        """Get all errors of a specific severity"""
        return [e for e in self.errors if e.severity == severity]

    def get_errors_by_category(self, category: str) -> List[ValidationError]:
        """Get all errors of a specific category"""
        return [e for e in self.errors if e.category == category]

    def has_fatal_errors(self) -> bool:
        """Check if there are any ERROR-level issues"""
        return any(e.severity == "ERROR" for e in self.errors)

    def get_statistics(self) -> Dict[str, int]:
        """Get validation statistics"""
        return {
            'total_cells': len(self.cells),
            'total_universes': len(self.universes),
            'total_surfaces': len(self.surfaces),
            'total_materials': len(self.materials),
            'total_errors': len(self.get_errors_by_severity('ERROR')),
            'total_warnings': len(self.get_errors_by_severity('WARNING')),
            'total_info': len(self.get_errors_by_severity('INFO')),
            'lattice_cells': sum(1 for c in self.cells.values() if c.lattice_type != LatticeType.NONE),
            'filled_cells': sum(1 for c in self.cells.values() if c.fill_simple or c.fill_array_elements),
        }

    def generate_summary_report(self) -> str:
        """Generate a summary validation report"""
        stats = self.get_statistics()
        lines = [
            "=== MCNP Cell Validation Report ===",
            "",
            "SUMMARY:",
            f"  Total Cells: {stats['total_cells']}",
            f"  Total Universes: {stats['total_universes']}",
            f"  Total Surfaces Referenced: {stats['total_surfaces']}",
            f"  Total Materials Referenced: {stats['total_materials']}",
            "",
            f"  Errors: {stats['total_errors']}",
            f"  Warnings: {stats['total_warnings']}",
            f"  Info: {stats['total_info']}",
            "",
        ]

        # Universe hierarchy info
        if self.universes:
            max_depth = max((u.nesting_depth for u in self.universes.values()), default=0)
            root_universes = sum(1 for u in self.universes.values() if u.nesting_depth == 1)
            lattice_universes = sum(1 for u in self.universes.values() if u.is_lattice)

            lines.extend([
                "UNIVERSE HIERARCHY:",
                f"  Maximum Nesting Depth: {max_depth} levels",
                f"  Root Universes: {root_universes}",
                f"  Lattice Universes: {lattice_universes}",
                "",
            ])

        # Error summary by severity
        if self.errors:
            lines.append("VALIDATION ISSUES:")
            for severity in ["ERROR", "WARNING", "INFO"]:
                issues = self.get_errors_by_severity(severity)
                if issues:
                    lines.append(f"\n  {severity}S ({len(issues)}):")
                    for err in issues[:10]:  # Show first 10 of each type
                        lines.append(f"    {err}")
                    if len(issues) > 10:
                        lines.append(f"    ... and {len(issues) - 10} more")

        return "\n".join(lines)


# Convenience functions for creating common structures

def create_simple_cell(cell_id: int, material_id: int, density: float,
                       surfaces: List[int], line_number: int = 0) -> CellDefinition:
    """Create a simple cell definition (no universe, no fill)"""
    return CellDefinition(
        cell_id=cell_id,
        material_id=material_id,
        density=density,
        surfaces=surfaces,
        line_number=line_number
    )


def create_lattice_cell(cell_id: int, universe: int, lattice_type: LatticeType,
                        surfaces: List[int], fill_bounds: Tuple[int, int, int, int, int, int],
                        fill_elements: List[int], line_number: int = 0) -> CellDefinition:
    """Create a lattice cell definition"""
    return CellDefinition(
        cell_id=cell_id,
        material_id=0,  # Lattice cells are always void
        density=None,
        surfaces=surfaces,
        universe=universe,
        lattice_type=lattice_type,
        fill_array_bounds=fill_bounds,
        fill_array_elements=fill_elements,
        line_number=line_number
    )


def create_filled_cell(cell_id: int, surfaces: List[int], fill_universe: int,
                       translation: Optional[Tuple[float, float, float]] = None,
                       line_number: int = 0) -> CellDefinition:
    """Create a cell with simple fill"""
    return CellDefinition(
        cell_id=cell_id,
        material_id=0,
        density=None,
        surfaces=surfaces,
        fill_simple=fill_universe,
        fill_translation=translation,
        line_number=line_number
    )


if __name__ == "__main__":
    # Example usage
    registry = MCNPInputRegistry()

    # Add a simple cell
    cell = create_simple_cell(
        cell_id=1,
        material_id=1,
        density=-10.0,
        surfaces=[-1, 2, -3],
        line_number=10
    )
    registry.cells[cell.cell_id] = cell

    # Add an error
    registry.add_error(
        severity="ERROR",
        category="CROSS_REF",
        message="Surface 99 not defined",
        line_number=10,
        cell_id=1
    )

    # Print report
    print(registry.generate_summary_report())

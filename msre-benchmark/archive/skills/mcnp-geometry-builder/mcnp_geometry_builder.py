"""MCNP Geometry Builder (Skill 2) - Build complex geometries interactively"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from typing import List, Tuple
from parsers.input_parser import SurfaceCard

class MCNPGeometryBuilder:
    def __init__(self):
        self.surfaces = []
        self.cells = []
        self.surf_counter = 1
        self.cell_counter = 1
        
    def add_sphere(self, surf_num: int, x: float, y: float, z: float, radius: float) -> int:
        """Add sphere surface with explicit surface number"""
        if x==0 and y==0 and z==0:
            self.surfaces.append(f"{surf_num} so {radius}")
        else:
            self.surfaces.append(f"{surf_num} s {x} {y} {z} {radius}")
        if surf_num >= self.surf_counter:
            self.surf_counter = surf_num + 1
        return surf_num
    
    def add_cylinder(self, axis: str, center: Tuple[float,float], radius: float) -> int:
        surf_num = self.surf_counter
        x,y = center
        self.surfaces.append(f"{surf_num} c/{axis.lower()} {x} {y} {radius}")
        self.surf_counter += 1
        return surf_num
    
    def add_plane(self, axis: str, position: float) -> int:
        surf_num = self.surf_counter
        self.surfaces.append(f"{surf_num} p{axis.lower()} {position}")
        self.surf_counter += 1
        return surf_num
    
    def add_box(self, xmin,xmax,ymin,ymax,zmin,zmax) -> int:
        surf_num = self.surf_counter
        self.surfaces.append(f"{surf_num} rpp {xmin} {xmax} {ymin} {ymax} {zmin} {zmax}")
        self.surf_counter += 1
        return surf_num
    
    def add_cell(self, cell_num: int, material: int, density: float, geometry: str, **params) -> int:
        """Add cell with explicit cell number"""
        cell_str = f"{cell_num} {material}"
        if density != 0:
            cell_str += f" {density}"
        cell_str += f" {geometry}"
        for k,v in params.items():
            # Convert importance_n to imp:n format
            if k.startswith('importance_'):
                particle = k.split('_')[1]
                cell_str += f" imp:{particle}={v}"
            else:
                cell_str += f" {k}={v}"
        self.cells.append(cell_str)
        if cell_num >= self.cell_counter:
            self.cell_counter = cell_num + 1
        return cell_num
    
    def generate_input(self) -> str:
        """Generate cell and surface cards (without title/data sections)"""
        output = []
        # Cells first
        output.extend(self.cells)
        output.append("")  # blank line
        # Surfaces second
        output.extend(self.surfaces)
        return "\n".join(output)

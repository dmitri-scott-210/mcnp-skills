"""MCNP Material Builder (Skill 3) - Create material specs with ZAID lookup"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from utils.zaid_database import ZAIDDatabase, ZAID
from utils.unit_conversions import UnitConverter

class MCNPMaterialBuilder:
    def __init__(self):
        self.zaid_db = ZAIDDatabase()
        self.materials = {}  # mat_num -> {'elements': [(zaid, fraction)], 'name': str}

    def add_material(self, mat_num: int, name: str = "") -> int:
        """Create a new material with given material number"""
        self.materials[mat_num] = {'elements': [], 'name': name or f"Material {mat_num}"}
        return mat_num

    def add_element(self, mat_num: int, element: str, fraction: float,
                    fraction_type: str = 'atom', library: str = "80c") -> None:
        """Add an element to a material

        Args:
            mat_num: Material number
            element: Element symbol (e.g., 'Al', 'Fe') or isotope (e.g., 'U-235')
            fraction: Atomic or mass fraction
            fraction_type: 'atom' or 'mass'
        """
        if mat_num not in self.materials:
            self.add_material(mat_num)

        # Get ZAID for element
        if '-' in element:
            # Isotope format like "U-235"
            zaid = self.zaid_db.isotope_to_zaid(element, library)
        else:
            # Element symbol like "Al" - use natural isotope
            # Map common elements to their natural isotope
            natural_isotopes = {
                'H': 'H-1', 'He': 'He-4', 'Li': 'Li-7', 'Be': 'Be-9', 'B': 'B-11',
                'C': 'C-12', 'N': 'N-14', 'O': 'O-16', 'F': 'F-19', 'Ne': 'Ne-20',
                'Na': 'Na-23', 'Mg': 'Mg-24', 'Al': 'Al-27', 'Si': 'Si-28', 'P': 'P-31',
                'S': 'S-32', 'Cl': 'Cl-35', 'Ar': 'Ar-40', 'K': 'K-39', 'Ca': 'Ca-40',
                'Fe': 'Fe-56', 'Cu': 'Cu-63', 'Zn': 'Zn-64', 'Pb': 'Pb-208', 'U': 'U-238'
            }

            if element in natural_isotopes:
                zaid = self.zaid_db.isotope_to_zaid(natural_isotopes[element], library)
            else:
                # Fall back to natural element (ZZZAAA where AAA=000)
                z = self.zaid_db.symbol_to_z(element)
                if z:
                    zaid = ZAID(z=z, a=0, library_id=library)
                else:
                    zaid = None

        if zaid:
            self.materials[mat_num]['elements'].append((str(zaid), fraction))

    def add_compound(self, mat_num: int, formula: str, library: str="80c") -> None:
        """Add a pre-defined compound to a material"""
        compounds = {
            "H2O": {"H-1": 2, "O-16": 1},
            "UO2": {"U-238": 1, "O-16": 2},
            "Al2O3": {"Al": 2, "O-16": 3}
        }
        if formula in compounds:
            if mat_num not in self.materials:
                self.add_material(mat_num, formula)
            for isotope, count in compounds[formula].items():
                self.add_element(mat_num, isotope, count, 'atom', library)
    
    def generate_cards(self) -> str:
        """Generate MCNP material cards"""
        lines = []
        for mat_num in sorted(self.materials.keys()):
            mat_data = self.materials[mat_num]
            # Material card
            line = f"m{mat_num}"
            for zaid, frac in mat_data['elements']:
                line += f" {zaid} {frac}"
            lines.append(line)
        return "\n".join(lines)

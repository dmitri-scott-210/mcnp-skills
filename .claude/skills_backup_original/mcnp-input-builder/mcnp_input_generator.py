"""
MCNP Input Generator (Skill 1)
Create new MCNP input files from high-level requirements
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from typing import Dict, List, Optional, Any, Tuple
from parsers.input_parser import MCNPInputParser, CellCard, SurfaceCard, DataCard
from utils.zaid_database import ZAIDDatabase
from utils.unit_conversions import UnitConverter


class MCNPInputGenerator:
    """
    Generate complete MCNP input files from problem specifications
    
    Capabilities:
    - Template-based generation for common problem types
    - Guided workflow for beginners
    - Automatic card creation with validation
    """
    
    def __init__(self):
        self.title = "MCNP Problem"
        self.cells = []
        self.surfaces = []
        self.data_cards = []
        self.zaid_db = ZAIDDatabase()
        
    def generate_simple_problem(self, problem_type: str, **kwargs) -> str:
        """
        Generate simple problem from type
        
        Types:
        - 'point_source_sphere': Point source in spherical shell
        - 'slab_shield': Slab shielding problem
        - 'criticality': Simple criticality problem
        
        Returns:
            MCNP input file content
        """
        if problem_type == 'point_source_sphere':
            return self._generate_point_source_sphere(**kwargs)
        elif problem_type == 'slab_shield':
            return self._generate_slab_shield(**kwargs)
        elif problem_type == 'criticality':
            return self._generate_criticality(**kwargs)
        else:
            raise ValueError(f"Unknown problem type: {problem_type}")
    
    def _generate_point_source_sphere(self, radius: float = 10.0, 
                                      material: str = "Al", 
                                      density: float = 2.7,
                                      source_energy: float = 14.1,
                                      n_particles: int = 1000000) -> str:
        """Generate point source in spherical geometry"""
        
        # Get ZAID for material
        zaid = self.zaid_db.isotope_to_zaid(material)
        
        input_lines = []
        input_lines.append(f"Point source in {material} sphere")

        # Cell cards (NO blank line after title!)
        input_lines.append(f"10   1  -{density}   -1    imp:n=1    $ {material} sphere")
        input_lines.append(f"20   0               1    imp:n=0    $ Outside (void)")
        input_lines.append("")
        
        # Surface cards
        input_lines.append("c Surface Cards")
        input_lines.append(f"1 so {radius}    $ Sphere at origin, radius={radius} cm")
        input_lines.append("")
        
        # Data cards
        input_lines.append("c Data Cards")
        input_lines.append(f"mode n")
        input_lines.append(f"nps {n_particles}")
        if zaid:
            input_lines.append(f"m1 {zaid} 1.0    $ {material}")
        else:
            input_lines.append(f"m1 13027 1.0    $ Aluminum (default)")
        input_lines.append(f"sdef pos=0 0 0 erg={source_energy}")
        input_lines.append(f"f1:n 1    $ Surface current across sphere")
        input_lines.append(f"f4:n 10   $ Track-length flux in sphere")
        input_lines.append(f"e1 0.1 99log 20")
        input_lines.append("")
        
        return '\n'.join(input_lines)
    
    def _generate_slab_shield(self, thickness: float = 10.0,
                             material: str = "H2O",
                             density: float = 1.0,
                             source_energy: float = 1.0,
                             n_particles: int = 10000000) -> str:
        """Generate slab shielding problem"""

        input_lines = []
        input_lines.append(f"Slab shield - {thickness} cm {material}")

        # Cell cards (NO blank line after title!)
        input_lines.append(f"10   0            -1          imp:n=1    $ Source region")
        input_lines.append(f"20   1  -{density}  1 -2      imp:n=1    $ Shield")
        input_lines.append(f"30   0              2 -3      imp:n=1    $ Detector region")
        input_lines.append(f"40   0              3         imp:n=0    $ Outside")
        input_lines.append("")
        
        # Surface cards
        input_lines.append("c Surface Cards")
        input_lines.append(f"1 pz 0              $ Source plane")
        input_lines.append(f"2 pz {thickness}    $ Far side of shield")
        input_lines.append(f"3 pz {thickness+50} $ Far boundary")
        input_lines.append("")
        
        # Data cards
        input_lines.append("c Data Cards")
        input_lines.append(f"mode n")
        input_lines.append(f"nps {n_particles}")
        
        # Material (simplified water)
        input_lines.append(f"m1 1001 2   $ H-1")
        input_lines.append(f"   8016 1   $ O-16")
        input_lines.append(f"mt1 lwtr.20t  $ Light water S(a,b)")
        
        # Source
        input_lines.append(f"sdef pos=0 0 -10 axs=0 0 1 ext=0 rad=d1 erg={source_energy}")
        input_lines.append(f"si1 0 10")
        input_lines.append(f"sp1 -21 1")
        
        # Tallies
        input_lines.append(f"f2:n 1    $ Source plane flux")
        input_lines.append(f"f12:n 2   $ Shield exit flux")
        input_lines.append(f"f22:n 3   $ Detector plane flux")
        input_lines.append("")
        
        return '\n'.join(input_lines)
    
    def _generate_criticality(self, fuel_radius: float = 5.0,
                             enrichment: float = 5.0,
                             cycles: Tuple[int, int, int] = (50, 20, 1000)) -> str:
        """Generate simple criticality problem"""
        
        inactive, active, particles = cycles

        input_lines = []
        input_lines.append(f"Simple criticality - {enrichment}% enriched U sphere")

        # Cell cards (NO blank line after title!)
        input_lines.append(f"10   1  -18.9  -1    imp:n=1    $ UO2 fuel")
        input_lines.append(f"20   0          1    imp:n=0    $ Outside")
        input_lines.append("")
        
        # Surface cards
        input_lines.append("c Surface Cards")
        input_lines.append(f"1 so {fuel_radius}    $ Fuel sphere")
        input_lines.append("")
        
        # Data cards
        input_lines.append("c Data Cards")
        input_lines.append(f"mode n")
        
        # Material - enriched uranium
        u235_frac = enrichment / 100.0
        u238_frac = 1.0 - u235_frac
        input_lines.append(f"m1 92235 {u235_frac}   $ U-235")
        input_lines.append(f"   92238 {u238_frac}   $ U-238")
        input_lines.append(f"   8016  2.0          $ O-16")
        
        # Criticality source
        input_lines.append(f"kcode {particles} 1.0 {inactive} {inactive+active}")
        input_lines.append(f"ksrc 0 0 0")
        input_lines.append("")
        
        return '\n'.join(input_lines)
    
    def generate_from_template(self, template_name: str, **params) -> str:
        """
        Generate from pre-defined template
        
        Templates: 'sphere', 'box', 'cylinder', 'lattice', 'reactor_unit_cell'
        """
        templates = {
            'sphere': self._generate_point_source_sphere,
            'slab': self._generate_slab_shield,
            'criticality': self._generate_criticality
        }
        
        if template_name in templates:
            return templates[template_name](**params)
        else:
            raise ValueError(f"Unknown template: {template_name}")
    
    def add_comments(self, input_text: str, comment: str, position: str = 'top') -> str:
        """Add comments to input file"""
        lines = input_text.split('\n')
        
        if position == 'top':
            lines.insert(1, f"c {comment}")
        elif position == 'bottom':
            lines.append(f"c {comment}")
        
        return '\n'.join(lines)


def main():
    """CLI interface for MCNP Input Generator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate MCNP input files')
    parser.add_argument('--type', required=True, choices=['sphere', 'slab', 'criticality'],
                       help='Problem type')
    parser.add_argument('--output', '-o', required=True, help='Output file path')
    parser.add_argument('--radius', type=float, default=10.0, help='Sphere radius (cm)')
    parser.add_argument('--thickness', type=float, default=10.0, help='Slab thickness (cm)')
    parser.add_argument('--material', default='Al', help='Material name')
    parser.add_argument('--density', type=float, default=2.7, help='Density (g/cm3)')
    parser.add_argument('--energy', type=float, default=14.1, help='Source energy (MeV)')
    parser.add_argument('--nps', type=int, default=1000000, help='Number of particles')
    
    args = parser.parse_args()
    
    generator = MCNPInputGenerator()
    
    if args.type == 'sphere':
        content = generator.generate_simple_problem('point_source_sphere',
                                                   radius=args.radius,
                                                   material=args.material,
                                                   density=args.density,
                                                   source_energy=args.energy,
                                                   n_particles=args.nps)
    elif args.type == 'slab':
        content = generator.generate_simple_problem('slab_shield',
                                                   thickness=args.thickness,
                                                   material=args.material,
                                                   density=args.density,
                                                   source_energy=args.energy,
                                                   n_particles=args.nps)
    elif args.type == 'criticality':
        content = generator.generate_simple_problem('criticality',
                                                   fuel_radius=args.radius)
    
    with open(args.output, 'w') as f:
        f.write(content)
    
    print(f"Generated MCNP input: {args.output}")
    print(f"Problem type: {args.type}")


if __name__ == "__main__":
    main()

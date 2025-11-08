"""MCNP Template Generator (Skill 6) - Pre-built templates for common problems"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

class MCNPTemplateGenerator:
    @staticmethod
    def reactor_unit_cell(pitch=1.26, fuel_radius=0.41, clad_thickness=0.07) -> str:
        """Generate PWR unit cell template

        Args:
            pitch: Lattice pitch in cm
            fuel_radius: Fuel pellet radius in cm
            clad_thickness: Cladding thickness in cm
        """
        clad_radius = fuel_radius + clad_thickness

        return f"""PWR Unit Cell - pitch={pitch} cm
10  1 -10.2 -1    u=1 imp:n=1 tmp=900  $ UO2 fuel
20  2  -6.6  1 -2 u=1 imp:n=1 tmp=600  $ Zircaloy clad
30  3 -0.74  2 -3 u=1 imp:n=1 tmp=600  $ Water moderator
40  0     -4    lat=1 fill=1 imp:n=1  $ Lattice cell
50  0      4    imp:n=0         $ Outside

1 cz {fuel_radius}
2 cz {clad_radius}
3 cz {pitch/2}
4 rpp -{pitch} {pitch} -{pitch} {pitch} -{pitch} {pitch}

mode n
kcode 10000 1.0 20 120
ksrc 0 0 0
m1 92235 -0.03 92238 -0.97 8016 -2.0  $ UO2 3% enriched
m2 40090 -0.50 40091 -0.11  $ Zircaloy
m3 1001 2 8016 1  $ Water
mt3 lwtr.20t
"""
    
    @staticmethod
    def dosimetry_sphere() -> str:
        """Generate dosimetry sphere template"""
        return """Dosimetry Sphere - ICRP geometry
10  1  -1.0  -1   imp:n,p=1  $ Water sphere
20  0        1    imp:n,p=0  $ Outside

1 so 15  $ 30cm diameter

mode n p
sdef pos=-20 0 0 erg=1.0 par=p
f6:p 10
nps 1000000
"""
    
    @staticmethod
    def shielding_slab(thickness=10) -> str:
        """Generate slab shielding template

        Args:
            thickness: Shield thickness in cm
        """
        return f"""Slab Shielding - {thickness} cm
10  0     -1      imp:n=1  $ Source region
20  1 -2.7  1 -2  imp:n=1  $ Shield
30  0      2 -3   imp:n=1  $ Detector region
40  0      3      imp:n=0  $ Outside

1 pz 0
2 pz {thickness}
3 pz {thickness+50}

mode n
nps 10000000
m1 13027 1.0  $ Aluminum
sdef pos=0 0 -10 erg=14.1
f2:n 1 2 3
"""

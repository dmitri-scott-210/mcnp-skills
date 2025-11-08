"""MCNP Source Builder (Skill 4) - Build complex source definitions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

class MCNPSourceBuilder:
    def __init__(self):
        self.sdef_params = {}
        self.distributions = []
        self.dist_counter = 1
        
    def set_position(self, x=0, y=0, z=0):
        self.sdef_params['pos'] = f"{x} {y} {z}"
    
    def set_energy(self, energy: float):
        self.sdef_params['erg'] = str(energy)
    
    def set_energy_distribution(self, energies: list, probabilities: list) -> int:
        dist_num = self.dist_counter
        self.sdef_params['erg'] = f"d{dist_num}"
        self.distributions.append(f"si{dist_num} L " + " ".join(map(str,energies)))
        self.distributions.append(f"sp{dist_num} " + " ".join(map(str,probabilities)))
        self.dist_counter += 1
        return dist_num
    
    def set_direction(self, u=0, v=0, w=1):
        self.sdef_params['vec'] = f"{u} {v} {w}"
        self.sdef_params['dir'] = "1"
    
    def set_particle_type(self, particle: str):
        self.sdef_params['par'] = particle.lower()
    
    def generate_sdef(self) -> str:
        """Generate SDEF card and distribution cards"""
        lines = []
        sdef = "sdef"
        for k,v in self.sdef_params.items():
            sdef += f" {k}={v}"
        lines.append(sdef)
        lines.extend(self.distributions)
        return "\n".join(lines)

    def generate_cards(self) -> str:
        """Alias for generate_sdef() for backwards compatibility"""
        return self.generate_sdef()
    
    def generate_criticality_source(self, n_particles=1000, n_cycles=100, n_skip=20, initial_guess=1.0, positions=None) -> str:
        lines = ["c Criticality Source"]
        lines.append(f"kcode {n_particles} {initial_guess} {n_skip} {n_cycles}")
        if positions:
            ksrc = "ksrc"
            for x,y,z in positions:
                ksrc += f" {x} {y} {z}"
            lines.append(ksrc)
        else:
            lines.append("ksrc 0 0 0")
        return "\n".join(lines)

"""MCNP Tally Builder (Skill 5) - Build tally specs with energy binning"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

class MCNPTallyBuilder:
    def __init__(self):
        self.tallies = []
        self.tally_counter = 1
        
    def add_surface_current(self, surfaces: list, particle='n') -> int:
        tally_num = self.tally_counter
        surf_list = " ".join(map(str,surfaces))
        self.tallies.append({'number':tally_num,'type':'F1','card':f"f{tally_num}:{particle} {surf_list}",'modifiers':[]})
        self.tally_counter += 1
        return tally_num
    
    def add_cell_flux(self, cells: list, particle='n') -> int:
        tally_num = self.tally_counter
        cell_list = " ".join(map(str,cells))
        self.tallies.append({'number':tally_num,'type':'F4','card':f"f{tally_num}:{particle} {cell_list}",'modifiers':[]})
        self.tally_counter += 1
        return tally_num
    
    def add_energy_deposition(self, cells: list, particle='n') -> int:
        tally_num = self.tally_counter
        cell_list = " ".join(map(str,cells))
        self.tallies.append({'number':tally_num,'type':'F6','card':f"f{tally_num}:{particle} {cell_list}",'modifiers':[]})
        self.tally_counter += 1
        return tally_num
    
    def add_energy_bins(self, tally_num: int, energies: list):
        for tally in self.tallies:
            if tally['number'] == tally_num:
                e_card = f"e{tally_num} " + " ".join(map(str,energies))
                tally['modifiers'].append(e_card)
                break
    
    def add_log_energy_bins(self, tally_num: int, emin: float, emax: float, nbins=100):
        for tally in self.tallies:
            if tally['number'] == tally_num:
                tally['modifiers'].append(f"e{tally_num} {emin} {nbins-1}log {emax}")
                break
    
    def add_comment(self, tally_num: int, comment: str):
        for tally in self.tallies:
            if tally['number'] == tally_num:
                tally['modifiers'].append(f"fc{tally_num} {comment}")
                break
    
    def generate_tallies(self) -> str:
        """Generate tally cards"""
        lines = []
        for tally in self.tallies:
            lines.append(tally['card'])
            lines.extend(tally['modifiers'])
        return "\n".join(lines)

    def generate_cards(self) -> str:
        """Alias for generate_tallies() for backwards compatibility"""
        return self.generate_tallies()

"""MCNP Variance Reducer (Skill 10) - Add importance, weight windows, DXTRAN"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.input_parser import MCNPInputParser, DataCard

class MCNPVarianceReducer:
    def __init__(self):
        self.parser = MCNPInputParser()
        self.parsed = None

    def load_file(self, filepath: str):
        """Load and parse MCNP input file"""
        self.parsed = self.parser.parse_file(filepath)
        return self.parsed

    def set_cell_importances(self, particle: str, importances: dict):
        """Set importance for cells: {cell_num: imp_value}"""
        if not self.parsed:
            self.parsed = {'data_cards': {}, 'cells': [], 'surfaces': [], 'title': '', 'message_block': []}

        imp_vals = []
        for cell in sorted(importances.keys()):
            imp_vals.append(str(importances[cell]))

        card_name = f"imp:{particle}"
        entries = imp_vals
        raw = f"{card_name} " + " ".join(entries)

        self.parsed['data_cards'][card_name] = DataCard(
            name=card_name,
            entries=entries,
            raw=raw
        )

    def add_weight_windows(self, particle: str, cells: list, energies: list, bounds: list):
        """Add WWN/WWE cards"""
        if not self.parsed:
            self.parsed = {'data_cards': {}, 'cells': [], 'surfaces': [], 'title': '', 'message_block': []}

        # WWN card
        card_name = f"wwn:{particle}"
        entries = list(map(str, bounds))
        raw = f"{card_name} " + " ".join(entries)
        self.parsed['data_cards'][card_name] = DataCard(name=card_name, entries=entries, raw=raw)

        # WWE card
        if energies:
            card_name = f"wwe:{particle}"
            entries = list(map(str, energies))
            raw = f"{card_name} " + " ".join(entries)
            self.parsed['data_cards'][card_name] = DataCard(name=card_name, entries=entries, raw=raw)

    def add_dxtran_sphere(self, position: tuple, radius: float, contribution: float = 0.9):
        """Add DXTRAN sphere for deep penetration"""
        if not self.parsed:
            self.parsed = {'data_cards': {}, 'cells': [], 'surfaces': [], 'title': '', 'message_block': []}

        x, y, z = position
        card_name = "dxt:n"
        entries = [str(radius), str(x), str(y), str(z), str(contribution)]
        raw = f"{card_name} " + " ".join(entries)
        self.parsed['data_cards'][card_name] = DataCard(name=card_name, entries=entries, raw=raw)

    def add_energy_cutoffs(self, particle: str, energy_cutoff: float):
        """Add energy cutoff"""
        if not self.parsed:
            self.parsed = {'data_cards': {}, 'cells': [], 'surfaces': [], 'title': '', 'message_block': []}

        card_name = f"cut:{particle}"
        entries = [str(energy_cutoff)]
        raw = f"{card_name} {energy_cutoff}"
        self.parsed['data_cards'][card_name] = DataCard(name=card_name, entries=entries, raw=raw)

    def save_file(self, filepath: str):
        """Save modified input to file"""
        if not self.parsed:
            return
        with open(filepath, 'w') as f:
            f.write(self.parser.to_string(self.parsed))

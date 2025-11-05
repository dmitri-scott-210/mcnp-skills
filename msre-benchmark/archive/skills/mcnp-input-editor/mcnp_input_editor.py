"""MCNP Input Editor (Skill 7) - Parse and edit existing MCNP files"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.input_parser import MCNPInputParser

class MCNPInputEditor:
    def __init__(self):
        self.parser = MCNPInputParser()
        self.parsed = None

    def load_file(self, filepath: str):
        """Load and parse MCNP input file"""
        self.parsed = self.parser.parse_file(filepath)
        return self.parsed

    def search_replace(self, old_text: str, new_text: str) -> int:
        """Search and replace text in cell cards"""
        if not self.parsed:
            return 0
        count = 0
        for cell in self.parsed['cells']:
            if old_text in cell.raw:
                cell.raw = cell.raw.replace(old_text, new_text)
                # Update parsed fields by re-parsing the modified line
                modified_cell = self.parser._parse_cell_card(cell.raw)
                if modified_cell:
                    cell.number = modified_cell.number
                    cell.material = modified_cell.material
                    cell.density = modified_cell.density
                    cell.geometry = modified_cell.geometry
                    cell.parameters = modified_cell.parameters
                count += 1
        return count

    def add_comment(self, text: str, position='top'):
        """Add comment to message block"""
        if not self.parsed:
            self.parsed = {'message_block': [], 'title': '', 'cells': [], 'surfaces': [], 'data_cards': {}}
        if position == 'top':
            self.parsed['message_block'].insert(0, f"c {text}")
        else:
            self.parsed['message_block'].append(f"c {text}")

    def remove_card(self, card_name: str):
        """Remove a data card by name"""
        if not self.parsed:
            return
        if card_name.lower() in self.parsed['data_cards']:
            del self.parsed['data_cards'][card_name.lower()]

    def save_file(self, filepath: str):
        """Save modified input to file"""
        if not self.parsed:
            return
        content = self.parser.to_string(self.parsed)
        with open(filepath, 'w') as f:
            f.write(content)

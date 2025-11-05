"""MCNP Input Updater (Skill 11) - Convert MCNP5 to MCNP6"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from parsers.input_parser import MCNPInputParser

class MCNPInputUpdater:
    def __init__(self):
        self.parser = MCNPInputParser()
        self.changes_made = []
        self.parsed = None

    def convert_mcnp5_to_mcnp6(self, input_file: str, output_file: str):
        """Convert MCNP5 input to MCNP6 format"""
        self.parsed = self.parser.parse_file(input_file)
        self.changes_made = []

        # Update library IDs .50c -> .80c (ENDF/B-VI -> ENDF/B-VIII)
        for card_name, card in self.parsed['data_cards'].items():
            if card_name.startswith('m'):  # Material cards
                for i, entry in enumerate(card.entries):
                    if '.50c' in entry:
                        card.entries[i] = entry.replace('.50c', '.80c')
                        self.changes_made.append(f"Updated {entry} to .80c library")
                    elif '.60c' in entry:
                        card.entries[i] = entry.replace('.60c', '.80c')
                        self.changes_made.append(f"Updated {entry} to .80c library")

        # Convert deprecated cards
        deprecated_map = {
            'notrn': 'phys:p',  # No transport -> physics options
            'pikmt': 'lcolr'    # Picket -> lost particle control
        }

        for old, new in deprecated_map.items():
            if old in self.parsed['data_cards']:
                card = self.parsed['data_cards'][old]
                del self.parsed['data_cards'][old]
                card.name = new
                self.parsed['data_cards'][new] = card
                self.changes_made.append(f"Converted {old.upper()} to {new.upper()}")

        # Write output
        with open(output_file, 'w') as f:
            f.write(self.parser.to_string(self.parsed))

        return self.changes_made

    def generate_migration_report(self) -> str:
        """Generate migration report"""
        report = ["MCNP5 to MCNP6 Migration Report", "=" * 50]
        report.append(f"Total changes: {len(self.changes_made)}")
        for change in self.changes_made:
            report.append(f"  - {change}")
        return "\n".join(report)

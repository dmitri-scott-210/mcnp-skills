"""
MCNP6.3 Input File Parser
Rewritten from scratch based on complete MCNP6.3 documentation

References:
- COMPLETE_MCNP6_KNOWLEDGE_BASE.md
- Chapter 4: Description of MCNP6 Input
- Chapter 5: Input Cards (all sections)

Author: Claude Code
Date: 2025-10-30
"""

import re
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class CellCard:
    """
    MCNP Cell Card
    Format: j m d geom params
    """
    number: int
    material: int  # 0 = void
    density: Optional[float] = None  # positive=atomic, negative=mass (g/cm³)
    geometry: str = ""  # CSG expression using surfaces
    parameters: Dict[str, Any] = field(default_factory=dict)
    raw: str = ""

    def __str__(self):
        parts = [str(self.number), str(self.material)]
        if self.density is not None:
            parts.append(str(self.density))
        if self.geometry:
            parts.append(self.geometry)
        for key, val in self.parameters.items():
            if isinstance(val, (list, tuple)):
                parts.append(f"{key}={' '.join(map(str, val))}")
            else:
                parts.append(f"{key}={val}")
        return " ".join(parts)


@dataclass
class SurfaceCard:
    """
    MCNP Surface Card
    Format: [*|+]j [n] A parameters
    """
    number: int
    mnemonic: str  # P, PX, SO, S, CZ, etc.
    parameters: List[float] = field(default_factory=list)
    transformation: Optional[int] = None
    reflecting: bool = False  # *
    white_boundary: bool = False  # +
    raw: str = ""

    def __str__(self):
        prefix = ""
        if self.reflecting:
            prefix = "*"
        elif self.white_boundary:
            prefix = "+"

        parts = [f"{prefix}{self.number}"]
        if self.transformation:
            parts.append(str(self.transformation))
        parts.append(self.mnemonic)
        parts.extend(map(str, self.parameters))
        return " ".join(parts)


@dataclass
class DataCard:
    """
    MCNP Data Card (MODE, NPS, M, SDEF, Fn, etc.)
    """
    name: str  # Card name (e.g., 'mode', 'm1', 'sdef', 'f4')
    entries: List[str] = field(default_factory=list)
    raw: str = ""

    def __str__(self):
        return f"{self.name} {' '.join(self.entries)}"


class MCNPInputParser:
    """
    MCNP6.3 Input Parser

    Parses MCNP input files according to specification:
    [MESSAGE BLOCK]
    <blank>
    TITLE
    CELL CARDS
    <blank>
    SURFACE CARDS
    <blank>
    DATA CARDS
    <blank>
    """

    def __init__(self):
        self.title = ""
        self.cells: List[CellCard] = []
        self.surfaces: List[SurfaceCard] = []
        self.data_cards: Dict[str, DataCard] = {}
        self.message_block: List[str] = []

    def parse_file(self, filepath: str) -> Dict[str, Any]:
        """Parse MCNP input file"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return self.parse_string(content)

    def parse_string(self, content: str) -> Dict[str, Any]:
        """
        Parse MCNP input from string

        Returns dict with: title, cells, surfaces, data_cards, message_block
        """
        # Reset state
        self.title = ""
        self.cells = []
        self.surfaces = []
        self.data_cards = {}
        self.message_block = []

        # Step 1: Process lines (remove comments, handle continuations)
        lines = self._process_lines(content)

        # Step 2: Split into blocks by blank lines
        blocks = self._split_into_blocks(lines)

        if len(blocks) < 3:
            # Need at least: title+cells, surfaces, data
            raise ValueError(f"MCNP input must have at least 3 blocks (cells, surfaces, data), found {len(blocks)}")

        # Step 3: Identify blocks
        # First block contains title (first line) and cells (remaining lines)
        title_and_cells = blocks[0]
        if title_and_cells:
            self.title = title_and_cells[0]
            cell_lines = title_and_cells[1:]
        else:
            cell_lines = []

        surface_lines = blocks[1] if len(blocks) > 1 else []
        data_lines = blocks[2] if len(blocks) > 2 else []

        # Step 4: Parse each block
        self._parse_cell_block(cell_lines)
        self._parse_surface_block(surface_lines)
        self._parse_data_block(data_lines)

        return {
            'title': self.title,
            'cells': self.cells,
            'surfaces': self.surfaces,
            'data_cards': self.data_cards,
            'message_block': self.message_block
        }

    def _process_lines(self, content: str) -> List[str]:
        """
        Process MCNP input lines:
        1. Remove comment lines (c in columns 1-5)
        2. Remove inline comments ($ to end of line)
        3. Join continuation lines (5+ leading spaces or &)
        4. PRESERVE BLANK LINES for block separation

        Returns list of processed lines
        """
        raw_lines = content.split('\n')
        processed = []
        current_card = ""

        for line in raw_lines:
            # Remove inline comments ($ and everything after)
            if '$' in line:
                line = line[:line.index('$')]

            # Check for blank line - preserve it
            if not line or line.isspace():
                # Save current card if any
                if current_card:
                    processed.append(current_card)
                    current_card = ""
                # Add blank line marker
                processed.append("")
                continue

            # Check for comment line (c in columns 1-5, followed by non-alphanumeric)
            if len(line) > 0 and line[0].lower() == 'c':
                # Check if it's actually a comment (c followed by space or end)
                if len(line) == 1 or not line[1].isalnum():
                    continue  # Skip this line

            # Check for continuation
            # Continuation = 5+ leading spaces OR starts with &
            stripped = line.lstrip()
            is_continuation = False

            if stripped.startswith('&'):
                is_continuation = True
                continuation_text = stripped[1:].strip()
            elif line.startswith('     '):  # 5+ spaces
                is_continuation = True
                continuation_text = stripped
            else:
                continuation_text = line.strip()

            if is_continuation and current_card:
                # Append to current card
                if continuation_text:
                    current_card += " " + continuation_text
            else:
                # Start new card
                if current_card:
                    processed.append(current_card)
                current_card = continuation_text

        # Don't forget last card
        if current_card:
            processed.append(current_card)

        return processed

    def _split_into_blocks(self, lines: List[str]) -> List[List[str]]:
        """
        Split lines into blocks separated by blank lines

        Blank line = empty or whitespace only
        """
        blocks = []
        current_block = []

        for line in lines:
            if not line or line.isspace():
                # Blank line - end current block
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            else:
                current_block.append(line)

        # Don't forget last block
        if current_block:
            blocks.append(current_block)

        return blocks

    def _parse_cell_block(self, lines: List[str]):
        """Parse cell cards from cell block"""
        for line in lines:
            if not line:
                continue

            try:
                cell = self._parse_cell_card(line)
                if cell:
                    self.cells.append(cell)
            except Exception as e:
                # Print warning but continue
                print(f"Warning: Failed to parse cell card: {line[:60]}...")
                print(f"  Error: {e}")

    def _parse_cell_card(self, line: str) -> Optional[CellCard]:
        """
        Parse single cell card

        Format: j m d geom params
        or: j LIKE n BUT list
        """
        parts = line.split()
        if len(parts) < 2:
            return None

        # Parse cell number
        try:
            cell_num = int(parts[0])
        except ValueError:
            return None

        # Check for LIKE n BUT format
        if len(parts) >= 3 and parts[1].upper() == 'LIKE':
            # TODO: Handle LIKE n BUT in future
            print(f"Warning: LIKE n BUT format not yet implemented: {line[:60]}...")
            return None

        # Parse material number
        try:
            material = int(parts[1])
        except ValueError:
            return None

        # Parse density (only if material != 0)
        density = None
        geom_start = 2

        if material != 0 and len(parts) > 2:
            try:
                density = float(parts[2])
                geom_start = 3
            except ValueError:
                # No density specified, geometry starts at position 2
                geom_start = 2

        # Parse geometry and parameters
        geometry_parts = []
        parameters = {}

        i = geom_start
        while i < len(parts):
            part = parts[i]

            # Check if this is a parameter (contains = or :)
            if '=' in part or (':' in part and i + 1 < len(parts) and '=' in parts[i + 1]):
                # This is a parameter
                # Handle both "IMP:N=1" and "IMP:N =1" and "IMP:N= 1"
                if '=' in part:
                    # Format: KEYWORD=value or KEYWORD:particle=value
                    key_val = part.split('=', 1)
                    param_key = key_val[0].upper().strip()
                    param_val_str = key_val[1].strip() if len(key_val) > 1 else ""
                else:
                    # Format: KEYWORD:particle (value comes next)
                    param_key = part.upper().strip()
                    param_val_str = ""

                # Collect value (may span multiple tokens until next parameter)
                value_parts = []
                if param_val_str:
                    value_parts.append(param_val_str)

                # Look ahead for more value parts
                j = i + 1
                while j < len(parts) and '=' not in parts[j] and ':' not in parts[j]:
                    value_parts.append(parts[j])
                    j += 1

                # Join value parts
                param_val = ' '.join(value_parts) if value_parts else ""

                # Try to convert to number
                try:
                    if '.' in param_val or 'e' in param_val.lower():
                        param_val = float(param_val)
                    else:
                        param_val = int(param_val)
                except ValueError:
                    pass  # Keep as string

                # Store parameter
                # Replace : with _ for particle-specific params
                param_key = param_key.replace(':', '_')
                parameters[param_key] = param_val

                # Skip to next parameter
                i = j
            else:
                # Part of geometry
                geometry_parts.append(part)
                i += 1

        geometry = " ".join(geometry_parts)

        return CellCard(
            number=cell_num,
            material=material,
            density=density,
            geometry=geometry,
            parameters=parameters,
            raw=line
        )

    def _parse_surface_block(self, lines: List[str]):
        """Parse surface cards from surface block"""
        for line in lines:
            if not line:
                continue

            try:
                surface = self._parse_surface_card(line)
                if surface:
                    self.surfaces.append(surface)
            except Exception as e:
                print(f"Warning: Failed to parse surface card: {line[:60]}...")
                print(f"  Error: {e}")

    def _parse_surface_card(self, line: str) -> Optional[SurfaceCard]:
        """
        Parse single surface card

        Format: [*|+]j [n] A parameters
        - * = reflecting
        - + = white boundary
        - j = surface number
        - n = optional transformation number
        - A = mnemonic (P, PX, SO, S, CZ, etc.)
        - parameters = numerical values
        """
        parts = line.split()
        if len(parts) < 2:
            return None

        # Check for reflecting (*) or white boundary (+)
        reflecting = False
        white_boundary = False
        surf_num_str = parts[0]

        if surf_num_str.startswith('*'):
            reflecting = True
            surf_num_str = surf_num_str[1:]
        elif surf_num_str.startswith('+'):
            white_boundary = True
            surf_num_str = surf_num_str[1:]

        # Parse surface number
        try:
            surf_num = int(surf_num_str)
        except ValueError:
            return None

        # Determine if next part is transformation number or mnemonic
        transformation = None
        mnemonic_idx = 1

        # Try to parse parts[1] as integer (transformation)
        try:
            transformation = int(parts[1])
            mnemonic_idx = 2
        except ValueError:
            # Not a number, must be mnemonic
            mnemonic_idx = 1

        if mnemonic_idx >= len(parts):
            return None

        # Parse mnemonic (always uppercase)
        mnemonic = parts[mnemonic_idx].upper()

        # Parse numerical parameters (everything after mnemonic)
        parameters = []
        for i in range(mnemonic_idx + 1, len(parts)):
            try:
                param = float(parts[i])
                parameters.append(param)
            except ValueError:
                # Stop at first non-number
                # Could be a keyword for macrobody, but basic surfaces are just numbers
                break

        return SurfaceCard(
            number=surf_num,
            mnemonic=mnemonic,
            parameters=parameters,
            transformation=transformation,
            reflecting=reflecting,
            white_boundary=white_boundary,
            raw=line
        )

    def _parse_data_block(self, lines: List[str]):
        """
        Parse data cards from data block

        Data cards can span multiple lines.
        Card name is in columns 1-5 (at start of line).
        Continuation lines start with spaces.
        """
        current_card_name = None
        current_card_entries = []
        current_card_raw = []

        for line in lines:
            if not line:
                continue

            # Check if line starts a new card (not indented)
            if not line[0].isspace():
                # Save previous card
                if current_card_name:
                    self.data_cards[current_card_name] = DataCard(
                        name=current_card_name,
                        entries=current_card_entries,
                        raw=' '.join(current_card_raw)
                    )

                # Start new card
                parts = line.split(None, 1)  # Split on first whitespace
                if parts:
                    current_card_name = parts[0].lower()
                    rest = parts[1] if len(parts) > 1 else ""
                    current_card_entries = rest.split() if rest else []
                    current_card_raw = [line]
            else:
                # Continuation of current card
                if current_card_name:
                    current_card_entries.extend(line.split())
                    current_card_raw.append(line)

        # Don't forget last card
        if current_card_name:
            self.data_cards[current_card_name] = DataCard(
                name=current_card_name,
                entries=current_card_entries,
                raw=' '.join(current_card_raw)
            )

    def get_cells_by_material(self, result: Dict[str, Any], material: int) -> List[CellCard]:
        """Get all cells using specified material"""
        return [cell for cell in result['cells'] if cell.material == material]

    def to_string(self, result: Dict[str, Any]) -> str:
        """
        Convert parsed result back to MCNP input string
        Useful for round-trip testing
        """
        lines = []

        # Title
        lines.append(result['title'])

        # Cells
        for cell in result['cells']:
            lines.append(str(cell))

        # Blank line
        lines.append('')

        # Surfaces
        for surface in result['surfaces']:
            lines.append(str(surface))

        # Blank line
        lines.append('')

        # Data cards
        for card in result['data_cards'].values():
            lines.append(str(card))

        return '\n'.join(lines)


# Test the parser
if __name__ == "__main__":
    import sys

    # Test with simple.txt
    simple_input = """simple - simplest MCNP input
10  0    -1   imp:n=1
20  0     1   imp:n=0

1 so    1.0

sdef
"""

    print("=" * 60)
    print("Testing MCNP6 Parser with simple.txt")
    print("=" * 60)

    parser = MCNPInputParser()
    result = parser.parse_string(simple_input)

    print(f"\nTitle: {result['title']}")
    print(f"\nCells: {len(result['cells'])}")
    for cell in result['cells']:
        print(f"  Cell {cell.number}: mat={cell.material}, density={cell.density}")
        print(f"    Geometry: {cell.geometry}")
        print(f"    Parameters: {cell.parameters}")

    print(f"\nSurfaces: {len(result['surfaces'])}")
    for surf in result['surfaces']:
        print(f"  Surface {surf.number}: {surf.mnemonic} {surf.parameters}")

    print(f"\nData cards: {list(result['data_cards'].keys())}")
    for name, card in result['data_cards'].items():
        print(f"  {name}: {' '.join(card.entries[:5])}{'...' if len(card.entries) > 5 else ''}")

    print("\n" + "=" * 60)
    print("Expected: 2 cells, 1 surface, 1 data card (sdef)")
    print("=" * 60)

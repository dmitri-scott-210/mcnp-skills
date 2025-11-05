#!/usr/bin/env python3
"""
Dependency Tree Builder

Builds universe dependency trees and detects circular references.
"""

import re
from collections import defaultdict, deque


class DependencyTreeBuilder:
    """Builds and analyzes universe dependency hierarchies"""

    def build_universe_tree(self, input_file):
        """
        Build complete universe dependency tree

        Args:
            input_file: Path to MCNP input file

        Returns:
            dict with keys:
                - 'universes': dict mapping universe_num to info dict
                - 'max_depth': int (maximum nesting level)
                - 'circular_refs': list of cycles found
        """
        with open(input_file, 'r') as f:
            lines = f.readlines()

        # Parse cell cards
        cell_cards = self._parse_cells(lines)

        # Initialize universe info
        universe_info = defaultdict(lambda: {
            'cells': [],
            'fills': [],
            'filled_by': [],
            'level': None
        })

        # Extract universe relationships
        all_universes = {0}  # Real world

        for cell_num, cell_line in cell_cards.items():
            # Get universe this cell belongs to
            u_match = re.search(r'\bu=(\d+)', cell_line, re.IGNORECASE)
            u_num = int(u_match.group(1)) if u_match else 0

            all_universes.add(u_num)
            universe_info[u_num]['cells'].append(cell_num)

            # Get universes this cell fills
            fill_match = re.search(r'\bfill=([^\s]+)', cell_line, re.IGNORECASE)
            if fill_match:
                fill_str = fill_match.group(1)

                # Simple fill
                if fill_str.isdigit():
                    fill_u = int(fill_str)
                    all_universes.add(fill_u)
                    universe_info[u_num]['fills'].append(fill_u)
                    universe_info[fill_u]['filled_by'].append(u_num)

                # Array fill
                else:
                    array_match = re.search(
                        r'fill=\s*-?\d+:-?\d+\s+-?\d+:-?\d+\s+-?\d+:-?\d+\s+([\d\s]+)',
                        cell_line,
                        re.IGNORECASE
                    )
                    if array_match:
                        universe_ids = array_match.group(1).split()
                        unique_fills = set(int(uid) for uid in universe_ids if uid.isdigit())

                        for fill_u in unique_fills:
                            all_universes.add(fill_u)
                            if fill_u not in universe_info[u_num]['fills']:
                                universe_info[u_num]['fills'].append(fill_u)
                                universe_info[fill_u]['filled_by'].append(u_num)

        # Calculate hierarchy levels (BFS from real world)
        queue = deque([(0, 0)])  # (universe_num, level)
        visited = {0}

        while queue:
            u, level = queue.popleft()
            universe_info[u]['level'] = level

            for fill_u in universe_info[u]['fills']:
                if fill_u not in visited:
                    visited.add(fill_u)
                    queue.append((fill_u, level + 1))

        # Find max depth
        max_depth = max(
            (info['level'] for info in universe_info.values() if info['level'] is not None),
            default=0
        )

        # Detect circular references
        circular_refs = self._find_cycles(universe_info, all_universes)

        return {
            'universes': dict(universe_info),
            'max_depth': max_depth,
            'circular_refs': circular_refs
        }

    def _find_cycles(self, universe_info, all_universes):
        """Detect circular universe references using DFS"""
        cycles = []
        visited = set()

        def dfs(u, rec_stack, path):
            """Depth-first search to find cycles"""
            visited.add(u)
            rec_stack.add(u)
            path.append(u)

            for fill_u in universe_info[u]['fills']:
                if fill_u not in visited:
                    if dfs(fill_u, rec_stack, path):
                        return True
                elif fill_u in rec_stack:
                    # Found cycle
                    cycle_start = path.index(fill_u)
                    cycle = path[cycle_start:] + [fill_u]
                    cycles.append(cycle)
                    return True

            rec_stack.remove(u)
            path.pop()
            return False

        # Check for cycles from each universe
        for u in all_universes:
            if u not in visited:
                dfs(u, set(), [])

        return cycles

    def _parse_cells(self, lines):
        """Parse cell cards from input file lines"""
        cell_cards = {}

        # Find cell cards block
        in_cells = False
        cell_lines = []
        blank_count = 0

        for i, line in enumerate(lines):
            if i == 0:  # Skip title
                continue

            # Count blank lines
            if line.strip() == '':
                blank_count += 1
                if blank_count >= 1:  # End of cells block
                    break
                continue

            # In cells block
            in_cells = True
            cell_lines.append(line)

        # Parse cell cards
        current_cell = ""
        for line in cell_lines:
            # Skip comments
            if line.strip().startswith('c '):
                continue

            # Handle continuation
            if line.strip().endswith('&'):
                current_cell += line.strip()[:-1] + " "
                continue
            else:
                current_cell += line.strip()

            # Process complete cell card
            if current_cell:
                parts = current_cell.split()
                if parts:
                    try:
                        cell_num = int(parts[0])
                        cell_cards[cell_num] = current_cell
                    except ValueError:
                        pass
                current_cell = ""

        return cell_cards

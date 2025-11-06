#!/usr/bin/env python3
"""
MCNP xsdir File Parser

Parse and query MCNP xsdir files to extract cross-section library information.

Usage:
    # Interactive mode
    python xsdir_parser.py

    # Command-line examples
    python xsdir_parser.py --zaid "92235.80c"
    python xsdir_parser.py --list-section neutron
    python xsdir_parser.py --search "92"
    python xsdir_parser.py --statistics
"""

import sys
import os
import argparse
import re
from collections import defaultdict


class XsdirEntry:
    """Represents a single xsdir entry"""

    def __init__(self, line, section='directory'):
        """
        Parse xsdir entry line

        Format: ZAID AWR filename access filelength recordlength entries temperature [ptable]
        """
        self.raw_line = line.strip()
        self.section = section

        parts = line.split()
        if len(parts) < 7:
            raise ValueError(f"Invalid xsdir entry: insufficient fields")

        self.zaid = parts[0]
        self.awr = float(parts[1])
        self.filename = parts[2]
        self.access = parts[3]
        self.file_length = int(parts[4])
        self.record_length = int(parts[5])
        self.entries = int(parts[6])
        self.temperature = float(parts[7]) if len(parts) > 7 else None
        self.ptable = int(parts[8]) if len(parts) > 8 else None

        # Parse ZAID components
        self._parse_zaid()

    def _parse_zaid(self):
        """Parse ZAID into components"""
        pattern = r'^(\d{1,3})(\d{3})\.(\d{2})([a-z])$'
        match = re.match(pattern, self.zaid, re.IGNORECASE)

        if match:
            self.z = int(match.group(1))
            self.a = int(match.group(2))
            self.library_num = match.group(3)
            self.library_type = match.group(4).lower()
        else:
            # Handle thermal scattering tables (e.g., lwtr.80t)
            thermal_pattern = r'^([a-z]+)\.(\d{2})([a-z])$'
            thermal_match = re.match(thermal_pattern, self.zaid, re.IGNORECASE)
            if thermal_match:
                self.z = None
                self.a = None
                self.material = thermal_match.group(1)
                self.library_num = thermal_match.group(2)
                self.library_type = thermal_match.group(3).lower()
            else:
                self.z = None
                self.a = None
                self.library_num = None
                self.library_type = None

    def get_temperature_k(self):
        """Convert temperature from MeV to Kelvin"""
        if self.temperature is not None:
            # kT (MeV) to T (K): T = kT / 8.617333E-11
            return self.temperature / 8.617333E-11
        return None

    def is_thermal_scattering(self):
        """Check if this is a thermal scattering table"""
        return hasattr(self, 'material') and self.material is not None

    def __str__(self):
        """String representation"""
        temp_k = self.get_temperature_k()
        temp_str = f"{temp_k:.1f} K" if temp_k else "N/A"

        if self.is_thermal_scattering():
            return f"{self.zaid:12s} AWR={self.awr:10.5f} T={temp_str:12s} [{self.section}]"
        else:
            isotope = f"Z={self.z} A={self.a}" if self.z is not None else "Unknown"
            return f"{self.zaid:12s} {isotope:12s} AWR={self.awr:10.5f} T={temp_str:12s} [{self.section}]"


class XsdirParser:
    """Parse and query MCNP xsdir files"""

    def __init__(self, xsdir_path=None):
        """
        Initialize parser

        Args:
            xsdir_path: Path to xsdir file (default: $DATAPATH/xsdir)
        """
        if xsdir_path is None:
            datapath = os.environ.get('DATAPATH')
            if not datapath:
                raise ValueError("DATAPATH not set. Set environment variable or provide xsdir_path.")
            xsdir_path = os.path.join(datapath, 'xsdir')

        if not os.path.exists(xsdir_path):
            raise FileNotFoundError(f"xsdir file not found: {xsdir_path}")

        self.xsdir_path = xsdir_path
        self.entries = []
        self.sections = defaultdict(list)
        self._parsed = False

    def parse(self):
        """Parse xsdir file"""
        if self._parsed:
            return

        current_section = 'header'

        with open(self.xsdir_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Skip comment lines
                if line.startswith('c ') or line.startswith('C '):
                    continue

                # Check for section markers
                line_lower = line.lower()
                if line_lower == 'directory':
                    current_section = 'directory'
                    continue
                elif line_lower == 'thermal':
                    current_section = 'thermal'
                    continue
                elif line_lower == 'photoatomic':
                    current_section = 'photoatomic'
                    continue
                elif line_lower == 'photoelectron' or line_lower == 'electron':
                    current_section = 'photoelectron'
                    continue
                elif line_lower == 'dosimetry':
                    current_section = 'dosimetry'
                    continue

                # Skip header section
                if current_section == 'header':
                    continue

                # Parse data entry
                try:
                    entry = XsdirEntry(line, current_section)
                    self.entries.append(entry)
                    self.sections[current_section].append(entry)
                except (ValueError, IndexError) as e:
                    # Skip invalid entries silently
                    continue

        self._parsed = True

    def find_zaid(self, zaid):
        """
        Find specific ZAID in xsdir

        Args:
            zaid: ZAID string (e.g., '92235.80c')

        Returns:
            XsdirEntry or None
        """
        self.parse()

        zaid_lower = zaid.lower()
        for entry in self.entries:
            if entry.zaid.lower() == zaid_lower:
                return entry

        return None

    def search(self, pattern, regex=False):
        """
        Search for ZAIDs matching pattern

        Args:
            pattern: Search pattern (substring or regex)
            regex: If True, treat pattern as regex

        Returns:
            list of XsdirEntry objects
        """
        self.parse()

        matches = []
        for entry in self.entries:
            if regex:
                if re.search(pattern, entry.zaid, re.IGNORECASE):
                    matches.append(entry)
            else:
                if pattern.lower() in entry.zaid.lower():
                    matches.append(entry)

        return matches

    def find_isotope(self, z, a=None, library_type='c'):
        """
        Find isotope by atomic number and mass number

        Args:
            z: Atomic number
            a: Mass number (None for natural element)
            library_type: Library type ('c', 't', 'p', etc.)

        Returns:
            list of XsdirEntry objects (may have multiple library versions)
        """
        self.parse()

        a_val = a if a is not None else 0
        zaid_pattern = f"{z}{a_val:03d}"

        matches = []
        for entry in self.entries:
            if (entry.z == z and entry.a == a_val and
                entry.library_type == library_type.lower()):
                matches.append(entry)

        return matches

    def get_statistics(self):
        """
        Get xsdir statistics

        Returns:
            dict with statistics
        """
        self.parse()

        stats = {
            'total_entries': len(self.entries),
            'sections': {},
            'library_types': defaultdict(int),
            'library_versions': defaultdict(int),
        }

        for section, entries in self.sections.items():
            stats['sections'][section] = len(entries)

        for entry in self.entries:
            if entry.library_type:
                stats['library_types'][entry.library_type] += 1
            if entry.library_num:
                lib_full = f".{entry.library_num}{entry.library_type}"
                stats['library_versions'][lib_full] += 1

        return stats

    def list_section(self, section):
        """
        List all entries in a section

        Args:
            section: Section name ('directory', 'thermal', etc.)

        Returns:
            list of XsdirEntry objects
        """
        self.parse()
        return self.sections.get(section, [])

    def get_all_zaids(self):
        """Get sorted list of all ZAIDs"""
        self.parse()
        return sorted([entry.zaid for entry in self.entries])


def interactive_mode(parser):
    """Interactive xsdir query mode"""
    print("=" * 70)
    print("MCNP xsdir Parser - Interactive Mode")
    print("=" * 70)
    print(f"xsdir file: {parser.xsdir_path}")
    print("\nCommands:")
    print("  find <ZAID>         - Find specific ZAID (e.g., 'find 92235.80c')")
    print("  search <pattern>    - Search for ZAIDs (e.g., 'search 92')")
    print("  isotope <Z> [A]     - Find isotope (e.g., 'isotope 92 235')")
    print("  section <name>      - List section ('directory', 'thermal', etc.)")
    print("  stats               - Show xsdir statistics")
    print("  list                - List all ZAIDs")
    print("  help                - Show this help")
    print("  quit, exit          - Exit program")
    print()

    while True:
        try:
            cmd = input("xsdir> ").strip()

            if not cmd:
                continue

            if cmd.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if cmd.lower() == 'help':
                print("\nAvailable commands:")
                print("  find 92235.80c      → Find U-235 ENDF/B-VIII.0")
                print("  search 92           → Search for all uranium isotopes")
                print("  isotope 92 235      → Find U-235 (all libraries)")
                print("  section thermal     → List thermal scattering tables")
                print("  stats               → Show library statistics")
                print("  list                → List all available ZAIDs")
                continue

            parts = cmd.split()
            command = parts[0].lower()

            if command == 'find':
                if len(parts) < 2:
                    print("ERROR: find requires a ZAID")
                    continue

                zaid = parts[1]
                entry = parser.find_zaid(zaid)

                if entry:
                    print(f"\nZAID: {entry.zaid}")
                    print(f"Section: {entry.section}")
                    print(f"Atomic Weight Ratio: {entry.awr:.6f}")
                    print(f"Filename: {entry.filename}")
                    temp_k = entry.get_temperature_k()
                    if temp_k:
                        print(f"Temperature: {temp_k:.1f} K ({entry.temperature:.4e} MeV)")
                    if entry.z is not None:
                        print(f"Z = {entry.z}, A = {entry.a}")
                    print(f"Library: .{entry.library_num}{entry.library_type}")
                else:
                    print(f"ZAID '{zaid}' not found in xsdir")

            elif command == 'search':
                if len(parts) < 2:
                    print("ERROR: search requires a pattern")
                    continue

                pattern = parts[1]
                matches = parser.search(pattern)

                if matches:
                    print(f"\nFound {len(matches)} matches for '{pattern}':")
                    for i, entry in enumerate(matches[:50], 1):
                        print(f"  {i:3d}. {entry}")
                    if len(matches) > 50:
                        print(f"  ... ({len(matches) - 50} more)")
                else:
                    print(f"No matches found for '{pattern}'")

            elif command == 'isotope':
                if len(parts) < 2:
                    print("ERROR: isotope requires Z [A]")
                    continue

                z = int(parts[1])
                a = int(parts[2]) if len(parts) > 2 else None

                matches = parser.find_isotope(z, a)

                if matches:
                    iso_name = f"Z={z}" + (f" A={a}" if a else " (natural)")
                    print(f"\nFound {len(matches)} libraries for {iso_name}:")
                    for entry in matches:
                        print(f"  {entry}")
                else:
                    print(f"No libraries found for Z={z}" + (f" A={a}" if a else ""))

            elif command == 'section':
                if len(parts) < 2:
                    print("ERROR: section requires name (directory, thermal, etc.)")
                    continue

                section_name = parts[1].lower()
                entries = parser.list_section(section_name)

                if entries:
                    print(f"\nSection '{section_name}' has {len(entries)} entries:")
                    for i, entry in enumerate(entries[:50], 1):
                        print(f"  {i:3d}. {entry.zaid:12s} AWR={entry.awr:10.5f}")
                    if len(entries) > 50:
                        print(f"  ... ({len(entries) - 50} more)")
                else:
                    print(f"Section '{section_name}' not found or empty")

            elif command == 'stats':
                stats = parser.get_statistics()

                print("\nxsdir Statistics:")
                print(f"Total entries: {stats['total_entries']}")
                print("\nBy section:")
                for section, count in sorted(stats['sections'].items()):
                    print(f"  {section:15s}: {count:5d} entries")

                print("\nBy library type:")
                for lib_type, count in sorted(stats['library_types'].items()):
                    type_name = {
                        'c': 'Continuous energy',
                        't': 'Thermal scattering',
                        'p': 'Photoatomic',
                        'e': 'Photoelectron',
                        'd': 'Discrete energy',
                        'y': 'Dosimetry',
                    }.get(lib_type, f'Type {lib_type}')
                    print(f"  .??{lib_type} ({type_name:20s}): {count:5d}")

                print("\nTop library versions:")
                sorted_versions = sorted(stats['library_versions'].items(),
                                       key=lambda x: x[1], reverse=True)
                for lib_ver, count in sorted_versions[:10]:
                    print(f"  {lib_ver:8s}: {count:5d}")

            elif command == 'list':
                zaids = parser.get_all_zaids()
                print(f"\nTotal ZAIDs: {len(zaids)}")
                print("First 50:")
                for i, zaid in enumerate(zaids[:50], 1):
                    print(f"  {i:3d}. {zaid}")
                if len(zaids) > 50:
                    print(f"  ... ({len(zaids) - 50} more)")
                print("\nUse 'search <pattern>' to filter results")

            else:
                print(f"ERROR: Unknown command '{command}'")
                print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nInterrupted. Type 'quit' to exit.")
        except Exception as e:
            print(f"ERROR: {e}")


def main():
    parser_arg = argparse.ArgumentParser(
        description='MCNP xsdir File Parser',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find specific ZAID
  python xsdir_parser.py --zaid "92235.80c"

  # Search for uranium isotopes
  python xsdir_parser.py --search "^92"

  # List thermal scattering tables
  python xsdir_parser.py --list-section thermal

  # Show statistics
  python xsdir_parser.py --statistics

  # Interactive mode (default)
  python xsdir_parser.py

Environment:
  DATAPATH: Path to MCNP data directory containing xsdir file
        """
    )

    parser_arg.add_argument('--xsdir', help='Path to xsdir file')
    parser_arg.add_argument('--zaid', help='Find specific ZAID')
    parser_arg.add_argument('--search', help='Search for ZAIDs matching pattern')
    parser_arg.add_argument('--isotope', nargs='+', help='Find isotope (Z [A])')
    parser_arg.add_argument('--list-section', help='List section (directory, thermal, etc.)')
    parser_arg.add_argument('--statistics', action='store_true', help='Show xsdir statistics')
    parser_arg.add_argument('--list-all', action='store_true', help='List all ZAIDs')

    args = parser_arg.parse_args()

    try:
        parser = XsdirParser(xsdir_path=args.xsdir)
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        print("\nPlease set DATAPATH environment variable or use --xsdir option")
        sys.exit(1)

    # Command-line mode
    if args.zaid:
        entry = parser.find_zaid(args.zaid)
        if entry:
            print(f"ZAID: {entry.zaid}")
            print(f"Section: {entry.section}")
            print(f"Atomic Weight Ratio: {entry.awr:.6f}")
            print(f"Filename: {entry.filename}")
            temp_k = entry.get_temperature_k()
            if temp_k:
                print(f"Temperature: {temp_k:.1f} K")
            if entry.z is not None:
                print(f"Z = {entry.z}, A = {entry.a}")
            sys.exit(0)
        else:
            print(f"ZAID '{args.zaid}' not found")
            sys.exit(1)

    elif args.search:
        matches = parser.search(args.search, regex=True)
        if matches:
            print(f"Found {len(matches)} matches:")
            for entry in matches:
                print(f"  {entry.zaid}")
        else:
            print(f"No matches found for '{args.search}'")
        sys.exit(0)

    elif args.isotope:
        z = int(args.isotope[0])
        a = int(args.isotope[1]) if len(args.isotope) > 1 else None
        matches = parser.find_isotope(z, a)

        if matches:
            print(f"Found {len(matches)} libraries:")
            for entry in matches:
                print(f"  {entry}")
            sys.exit(0)
        else:
            print(f"No libraries found")
            sys.exit(1)

    elif args.list_section:
        entries = parser.list_section(args.list_section)
        if entries:
            print(f"Section '{args.list_section}' ({len(entries)} entries):")
            for entry in entries:
                print(f"  {entry.zaid}")
        else:
            print(f"Section '{args.list_section}' not found or empty")
        sys.exit(0)

    elif args.statistics:
        stats = parser.get_statistics()
        print("xsdir Statistics:")
        print(f"Total entries: {stats['total_entries']}")
        print("\nBy section:")
        for section, count in sorted(stats['sections'].items()):
            print(f"  {section}: {count}")
        print("\nBy library type:")
        for lib_type, count in sorted(stats['library_types'].items()):
            print(f"  .??{lib_type}: {count}")
        sys.exit(0)

    elif args.list_all:
        zaids = parser.get_all_zaids()
        for zaid in zaids:
            print(zaid)
        sys.exit(0)

    else:
        # Interactive mode (default)
        interactive_mode(parser)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
MCNP Missing Library Diagnoser

Diagnose and troubleshoot MCNP cross-section library errors with systematic
debugging procedures and fix recommendations.

Usage:
    # Diagnose MCNP error message
    python missing_library_diagnoser.py --error "cross-section table 92235.80c not found"

    # Check input file for missing libraries
    python missing_library_diagnoser.py --input input.i

    # Verify DATAPATH setup
    python missing_library_diagnoser.py --verify-setup

    # Interactive mode
    python missing_library_diagnoser.py
"""

import sys
import os
import argparse
import re
from pathlib import Path


class LibraryDiagnoser:
    """Diagnose MCNP library errors"""

    def __init__(self, datapath=None):
        """
        Initialize diagnoser

        Args:
            datapath: Path to MCNP data directory (default: $DATAPATH env var)
        """
        self.datapath = datapath or os.environ.get('DATAPATH')
        self.xsdir_path = None

        if self.datapath:
            self.xsdir_path = os.path.join(self.datapath, 'xsdir')

    def verify_setup(self):
        """
        Verify MCNP cross-section library setup

        Returns:
            dict with verification results
        """
        results = {
            'checks': [],
            'errors': [],
            'warnings': [],
            'recommendations': []
        }

        # Check 1: DATAPATH set
        if not self.datapath:
            results['errors'].append("DATAPATH environment variable not set")
            results['recommendations'].append(
                "Set DATAPATH: export DATAPATH=/path/to/mcnpdata (Linux) or "
                "set DATAPATH=C:\\mcnpdata (Windows)"
            )
        else:
            results['checks'].append(f"DATAPATH set: {self.datapath}")

            # Check 2: DATAPATH exists
            if not os.path.exists(self.datapath):
                results['errors'].append(f"DATAPATH directory does not exist: {self.datapath}")
                results['recommendations'].append(
                    "Verify DATAPATH points to correct directory containing MCNP data"
                )
            else:
                results['checks'].append(f"DATAPATH directory exists")

                # Check 3: xsdir exists
                if not os.path.exists(self.xsdir_path):
                    results['errors'].append(f"xsdir file not found: {self.xsdir_path}")
                    results['recommendations'].append(
                        "Verify MCNP data libraries installed completely"
                    )
                else:
                    results['checks'].append(f"xsdir file found")

                    # Check 4: xsdir readable
                    try:
                        with open(self.xsdir_path, 'r') as f:
                            f.read(100)
                        results['checks'].append("xsdir file readable")
                    except Exception as e:
                        results['errors'].append(f"Cannot read xsdir: {e}")
                        results['recommendations'].append(
                            "Check file permissions: chmod +r xsdir (Linux)"
                        )

                    # Check 5: xsdir size reasonable
                    try:
                        size = os.path.getsize(self.xsdir_path)
                        if size < 10000:  # Less than 10 KB
                            results['warnings'].append(
                                f"xsdir file very small ({size} bytes) - may be incomplete"
                            )
                            results['recommendations'].append(
                                "Verify complete library installation"
                            )
                        else:
                            results['checks'].append(f"xsdir size: {size:,} bytes")
                    except Exception:
                        pass

        return results

    def diagnose_error(self, error_message):
        """
        Diagnose MCNP error message

        Args:
            error_message: Error message from MCNP output

        Returns:
            dict with diagnosis and recommendations
        """
        diagnosis = {
            'error_type': None,
            'zaid': None,
            'problem': None,
            'causes': [],
            'fixes': []
        }

        # Error pattern 1: "cross-section table (ZAID) not found"
        pattern1 = r'cross-section table\s+(\S+)\s+not found'
        match = re.search(pattern1, error_message, re.IGNORECASE)

        if match:
            zaid = match.group(1)
            diagnosis['error_type'] = 'ZAID_NOT_FOUND'
            diagnosis['zaid'] = zaid
            diagnosis['problem'] = f"Cross-section table {zaid} not found in xsdir"

            diagnosis['causes'] = [
                "DATAPATH not set or incorrect",
                f"{zaid} not in xsdir file (library not installed)",
                "Wrong library version specified",
                "xsdir file corrupted or incomplete"
            ]

            diagnosis['fixes'] = [
                f"Check if DATAPATH set: echo $DATAPATH (Linux) or echo %DATAPATH% (Windows)",
                f"Search xsdir for {zaid}: grep '{zaid}' $DATAPATH/xsdir",
                f"Try alternative library version (e.g., .70c instead of .80c)",
                "Use natural element (e.g., 92000.80c for natural uranium)",
                "Verify library installation is complete"
            ]

            return diagnosis

        # Error pattern 2: "cannot open file"
        pattern2 = r'cannot open file\s+(\S+)'
        match = re.search(pattern2, error_message, re.IGNORECASE)

        if match:
            filepath = match.group(1)
            diagnosis['error_type'] = 'CANNOT_OPEN_FILE'
            diagnosis['problem'] = f"Cannot open cross-section file: {filepath}"

            diagnosis['causes'] = [
                "File does not exist at specified path",
                "DATAPATH incorrect (xsdir paths relative to DATAPATH)",
                "File permissions deny read access",
                "Network drive issue or disconnection",
                "Path contains invalid characters or spaces"
            ]

            diagnosis['fixes'] = [
                f"Check if file exists: ls {filepath} (Linux) or dir {filepath} (Windows)",
                "Verify DATAPATH points to correct directory",
                "Check file permissions: ls -l (Linux)",
                "If on network drive, check connection and permissions",
                "Verify xsdir entry matches actual file location"
            ]

            return diagnosis

        # Error pattern 3: "AWR is zero"
        pattern3 = r'atomic weight ratio.*is zero|AWR.*0\.0+'
        match = re.search(pattern3, error_message, re.IGNORECASE)

        if match:
            diagnosis['error_type'] = 'AWR_ZERO'
            diagnosis['problem'] = "Atomic weight ratio (AWR) is zero or invalid"

            diagnosis['causes'] = [
                "xsdir file corrupted",
                "xsdir entry edited incorrectly",
                "Library installation incomplete or damaged"
            ]

            diagnosis['fixes'] = [
                "Restore xsdir from backup: cp $DATAPATH/xsdir.backup $DATAPATH/xsdir",
                "Check xsdir entry for ZAID (second field should be AWR)",
                "Regenerate xsdir or reinstall libraries",
                "Verify ZAID entry has correct format"
            ]

            return diagnosis

        # Error pattern 4: "temperature out of range"
        pattern4 = r'temperature.*out of range'
        match = re.search(pattern4, error_message, re.IGNORECASE)

        if match:
            diagnosis['error_type'] = 'TEMPERATURE_OUT_OF_RANGE'
            diagnosis['problem'] = "Requested temperature not available for library"

            diagnosis['causes'] = [
                "TMP card specifies temperature outside library range",
                "Temperature-specific library not installed",
                "Library only available at default temperature"
            ]

            diagnosis['fixes'] = [
                "Check available temperature libraries in xsdir",
                "Use higher temperature library + TMP interpolation",
                "Accept default temperature (MCNP will warn but continue)",
                "Remove TMP card if temperature effects negligible"
            ]

            return diagnosis

        # Generic error
        diagnosis['error_type'] = 'UNKNOWN'
        diagnosis['problem'] = "Unrecognized library error"
        diagnosis['fixes'] = [
            "Run setup verification: python missing_library_diagnoser.py --verify-setup",
            "Check MCNP output for complete error message",
            "Verify DATAPATH and xsdir file",
            "Check input file for invalid ZAID specifications"
        ]

        return diagnosis

    def check_input_file(self, input_file):
        """
        Check MCNP input file for missing libraries

        Args:
            input_file: Path to MCNP input file

        Returns:
            dict with results
        """
        if not os.path.exists(input_file):
            return {'error': f"Input file not found: {input_file}"}

        # Extract ZAIDs from input
        zaids_found = set()
        zaid_pattern = r'\b(\d{1,3}\d{3}\.\d{2}[a-z])\b'

        with open(input_file, 'r') as f:
            for line in f:
                if line.strip().startswith('c ') or line.strip().startswith('C '):
                    continue
                matches = re.findall(zaid_pattern, line, re.IGNORECASE)
                zaids_found.update([m.lower() for m in matches])

        if not zaids_found:
            return {
                'total': 0,
                'message': 'No ZAIDs found in input file'
            }

        # Check each ZAID
        if not self.xsdir_path or not os.path.exists(self.xsdir_path):
            return {
                'error': 'Cannot check ZAIDs: xsdir not available',
                'zaids_found': sorted(zaids_found)
            }

        # Load xsdir ZAIDs
        xsdir_zaids = set()
        with open(self.xsdir_path, 'r', encoding='utf-8', errors='ignore') as f:
            in_directory = False
            for line in f:
                line = line.strip()
                if not line or line.startswith('c '):
                    continue

                if line.lower() == 'directory':
                    in_directory = True
                    continue
                elif line.lower() in ['thermal', 'photoatomic', 'photoelectron']:
                    in_directory = False

                if in_directory:
                    parts = line.split()
                    if len(parts) >= 1:
                        xsdir_zaids.add(parts[0].lower())

        # Check availability
        available = []
        missing = []

        for zaid in sorted(zaids_found):
            if zaid in xsdir_zaids:
                available.append(zaid)
            else:
                missing.append(zaid)

        return {
            'total': len(zaids_found),
            'available': available,
            'missing': missing,
            'input_file': input_file
        }


def interactive_mode(diagnoser):
    """Interactive diagnosis mode"""
    print("=" * 70)
    print("MCNP Missing Library Diagnoser - Interactive Mode")
    print("=" * 70)

    if diagnoser.datapath:
        print(f"DATAPATH: {diagnoser.datapath}")
    else:
        print("WARNING: DATAPATH not set")

    print("\nCommands:")
    print("  verify              - Verify DATAPATH and library setup")
    print("  diagnose <error>    - Diagnose error message")
    print("  check <file>        - Check input file for missing libraries")
    print("  help                - Show this help")
    print("  quit, exit          - Exit program")
    print()

    while True:
        try:
            cmd = input("diagnose> ").strip()

            if not cmd:
                continue

            if cmd.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if cmd.lower() == 'help':
                print("\nAvailable commands:")
                print("  verify                      → Verify library setup")
                print("  diagnose <error message>    → Diagnose error")
                print("  check input.i               → Check input file")
                continue

            parts = cmd.split(None, 1)
            command = parts[0].lower()

            if command == 'verify':
                results = diagnoser.verify_setup()

                print("\nSetup Verification:")
                print("=" * 60)

                if results['checks']:
                    print("\nPassed checks:")
                    for check in results['checks']:
                        print(f"  ✓ {check}")

                if results['warnings']:
                    print("\nWarnings:")
                    for warning in results['warnings']:
                        print(f"  ⚠ {warning}")

                if results['errors']:
                    print("\nErrors:")
                    for error in results['errors']:
                        print(f"  ✗ {error}")

                if results['recommendations']:
                    print("\nRecommendations:")
                    for i, rec in enumerate(results['recommendations'], 1):
                        print(f"  {i}. {rec}")

            elif command == 'diagnose':
                if len(parts) < 2:
                    print("ERROR: diagnose requires an error message")
                    continue

                error_msg = parts[1]
                diagnosis = diagnoser.diagnose_error(error_msg)

                print("\nDiagnosis:")
                print("=" * 60)
                print(f"Error type: {diagnosis['error_type']}")

                if diagnosis['zaid']:
                    print(f"ZAID: {diagnosis['zaid']}")

                print(f"\nProblem: {diagnosis['problem']}")

                if diagnosis['causes']:
                    print("\nPossible causes:")
                    for i, cause in enumerate(diagnosis['causes'], 1):
                        print(f"  {i}. {cause}")

                if diagnosis['fixes']:
                    print("\nRecommended fixes:")
                    for i, fix in enumerate(diagnosis['fixes'], 1):
                        print(f"  {i}. {fix}")

            elif command == 'check':
                if len(parts) < 2:
                    print("ERROR: check requires an input file")
                    continue

                input_file = parts[1]
                result = diagnoser.check_input_file(input_file)

                if 'error' in result:
                    print(f"\nERROR: {result['error']}")
                    if 'zaids_found' in result:
                        print(f"ZAIDs in input: {', '.join(result['zaids_found'])}")
                    continue

                print(f"\nInput file: {result['input_file']}")
                print(f"Total ZAIDs: {result['total']}")
                print(f"Available: {len(result['available'])}")
                print(f"Missing: {len(result['missing'])}")

                if result['missing']:
                    print("\nMissing ZAIDs:")
                    for zaid in result['missing']:
                        print(f"  ✗ {zaid}")

                    print("\nRecommendations:")
                    print("  1. Use 'diagnose' command for each missing ZAID")
                    print("  2. Check alternative library versions")
                    print("  3. Use natural element mix if specific isotope unavailable")
                else:
                    print("\n✓ All ZAIDs are available")

            else:
                print(f"ERROR: Unknown command '{command}'")
                print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nInterrupted. Type 'quit' to exit.")
        except Exception as e:
            print(f"ERROR: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='MCNP Missing Library Diagnoser',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Verify setup
  python missing_library_diagnoser.py --verify-setup

  # Diagnose error
  python missing_library_diagnoser.py --error "cross-section table 92235.80c not found"

  # Check input file
  python missing_library_diagnoser.py --input input.i

  # Interactive mode (default)
  python missing_library_diagnoser.py

Environment:
  DATAPATH: Path to MCNP data directory containing xsdir file
        """
    )

    parser.add_argument('--datapath', help='Path to MCNP data directory')
    parser.add_argument('--verify-setup', action='store_true', help='Verify library setup')
    parser.add_argument('--error', help='Diagnose error message')
    parser.add_argument('--input', help='Check input file for missing libraries')

    args = parser.parse_args()

    diagnoser = LibraryDiagnoser(datapath=args.datapath)

    # Command-line mode
    if args.verify_setup:
        results = diagnoser.verify_setup()

        print("Setup Verification:")
        print("=" * 60)

        for check in results['checks']:
            print(f"✓ {check}")

        for warning in results['warnings']:
            print(f"⚠ {warning}")

        for error in results['errors']:
            print(f"✗ {error}")

        if results['recommendations']:
            print("\nRecommendations:")
            for i, rec in enumerate(results['recommendations'], 1):
                print(f"{i}. {rec}")

        sys.exit(0 if not results['errors'] else 1)

    elif args.error:
        diagnosis = diagnoser.diagnose_error(args.error)

        print(f"Error type: {diagnosis['error_type']}")
        if diagnosis['zaid']:
            print(f"ZAID: {diagnosis['zaid']}")
        print(f"\nProblem: {diagnosis['problem']}")

        if diagnosis['causes']:
            print("\nPossible causes:")
            for cause in diagnosis['causes']:
                print(f"  - {cause}")

        if diagnosis['fixes']:
            print("\nRecommended fixes:")
            for i, fix in enumerate(diagnosis['fixes'], 1):
                print(f"{i}. {fix}")

        sys.exit(0)

    elif args.input:
        result = diagnoser.check_input_file(args.input)

        if 'error' in result:
            print(f"ERROR: {result['error']}")
            sys.exit(1)

        print(f"Input file: {result['input_file']}")
        print(f"Total ZAIDs: {result['total']}")
        print(f"Available: {len(result['available'])}")
        print(f"Missing: {len(result['missing'])}")

        if result['missing']:
            print("\nMissing ZAIDs:")
            for zaid in result['missing']:
                print(f"  {zaid}")
            sys.exit(1)
        else:
            print("\nAll ZAIDs are available ✓")
            sys.exit(0)

    else:
        # Interactive mode (default)
        interactive_mode(diagnoser)


if __name__ == '__main__':
    main()

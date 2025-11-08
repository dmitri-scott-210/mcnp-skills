"""
MCNP Cross-Section Library Consistency Checker

Detects mixed ENDF library versions in MCNP input files.
Based on AGR-1 Material Card Analysis findings showing mixed .00c, .70c, and .80c libraries.

Mixed libraries can cause:
- Inconsistent cross-section data
- Validation issues
- Benchmark failures
"""

import re
from typing import Dict, List, Tuple
from collections import defaultdict

class LibraryConsistencyChecker:
    """Check for mixed ENDF library versions in MCNP materials"""

    # ENDF library version mapping
    ENDF_VERSIONS = {
        '00': 'ENDF/B-VI.0',
        '50': 'ENDF/B-V',
        '60': 'ENDF/B-VI.8',
        '70': 'ENDF/B-VII.0',
        '71': 'ENDF/B-VII.1',
        '80': 'ENDF/B-VIII.0',
        '20': 'Special (B-10 optimized)',
        '55': 'Special (Tungsten)',
        '66': 'ENDF/B-VI.6',
        '31': 'ENDF/B-VI.2',
        '42': 'ENDF/B-VI.4',
    }

    # Library type suffixes
    LIBRARY_TYPES = {
        'c': 'Continuous-energy neutron',
        'p': 'Photoatomic',
        'u': 'Photonuclear',
        'e': 'Electron',
        't': 'Thermal scattering S(α,β)',
        'd': 'Discrete reaction',
        'm': 'Multigroup',
    }

    def __init__(self):
        self.warnings = []
        self.info = []

    def check_consistency(self, materials: Dict[str, Dict[str, float]]) -> Dict:
        """
        Check for mixed ENDF library versions

        Args:
            materials: {mat_id: {zaid: fraction}}

        Returns:
            {'warnings': [...], 'info': [...], 'summary': {...}}
        """
        self.warnings = []
        self.info = []

        # Analyze library versions used
        library_usage = self._analyze_library_versions(materials)

        # Check for mixed versions
        if len(library_usage) > 1:
            self._generate_mixed_library_warning(library_usage, materials)
        else:
            self._generate_consistent_library_info(library_usage)

        return self._format_results(library_usage)

    def _analyze_library_versions(self, materials: Dict) -> Dict:
        """
        Analyze which library versions are used

        Returns:
            {version: {'materials': [...], 'zaids': [...], 'count': int}}
        """
        library_usage = defaultdict(lambda: {'materials': set(), 'zaids': [], 'count': 0})

        for mat_id, isotopes in materials.items():
            for zaid, fraction in isotopes.items():
                # Extract library version from ZAID (e.g., '92235.80c' → '80')
                version_info = self._extract_version(zaid)

                if version_info:
                    version, lib_type = version_info
                    library_usage[version]['materials'].add(mat_id)
                    library_usage[version]['zaids'].append(zaid)
                    library_usage[version]['count'] += 1

        # Convert sets to lists for JSON serialization
        for version in library_usage:
            library_usage[version]['materials'] = sorted(list(library_usage[version]['materials']))

        return dict(library_usage)

    def _extract_version(self, zaid: str) -> Tuple[str, str]:
        """
        Extract library version and type from ZAID

        Args:
            zaid: e.g., '92235.80c', '1001.70c', '6000.24p'

        Returns:
            (version, type) e.g., ('80', 'c') or None
        """
        # Match pattern: ZZZAAA.XXt where XX is version, t is type
        match = re.match(r'\d+\.(\d+)([a-z])', str(zaid).lower())

        if match:
            version = match.group(1)
            lib_type = match.group(2)
            return (version, lib_type)

        return None

    def _generate_mixed_library_warning(self, library_usage: Dict, materials: Dict):
        """Generate warning for mixed library versions"""

        # Create detailed breakdown
        version_details = []
        for version, info in sorted(library_usage.items()):
            endf_name = self.ENDF_VERSIONS.get(version, f'Unknown ({version})')
            version_details.append({
                'version': version,
                'endf_name': endf_name,
                'material_count': len(info['materials']),
                'isotope_count': info['count'],
                'materials': info['materials'][:10],  # First 10 materials
            })

        # Main warning
        self.warnings.append({
            'type': 'MIXED_LIBRARY_VERSIONS',
            'severity': 'WARNING',
            'message': f'Found {len(library_usage)} different ENDF library versions in use',
            'impact': 'May cause inconsistencies in cross-section data, benchmark issues',
            'recommendation': 'Standardize to ENDF/B-VIII.0 (.80c) or ENDF/B-VII.0 (.70c)',
            'versions': version_details
        })

        # Identify recommended target version
        if '80' in library_usage:
            target = '80 (ENDF/B-VIII.0)'
        elif '71' in library_usage:
            target = '71 (ENDF/B-VII.1)'
        elif '70' in library_usage:
            target = '70 (ENDF/B-VII.0)'
        else:
            target = '80 (ENDF/B-VIII.0) - latest'

        self.warnings.append({
            'type': 'LIBRARY_STANDARDIZATION_RECOMMENDATION',
            'severity': 'INFO',
            'message': f'Recommend standardizing all materials to .{target}',
            'reason': 'Ensures consistent cross-section data across all materials',
            'action': 'Review materials and update ZAID library versions'
        })

    def _generate_consistent_library_info(self, library_usage: Dict):
        """Generate info message for consistent libraries"""

        if len(library_usage) == 1:
            version = list(library_usage.keys())[0]
            endf_name = self.ENDF_VERSIONS.get(version, f'Version {version}')

            self.info.append({
                'type': 'CONSISTENT_LIBRARY_VERSION',
                'message': f'All materials use consistent library version: {endf_name} (.{version}c)',
                'version': version,
                'endf_name': endf_name,
                'material_count': len(library_usage[version]['materials'])
            })

    def _format_results(self, library_usage: Dict) -> Dict:
        """Format validation results"""

        summary = {
            'version_count': len(library_usage),
            'is_consistent': len(library_usage) <= 1,
            'versions_used': {
                v: {
                    'endf_name': self.ENDF_VERSIONS.get(v, f'Unknown ({v})'),
                    'material_count': len(info['materials']),
                    'isotope_count': info['count']
                }
                for v, info in library_usage.items()
            }
        }

        return {
            'warnings': self.warnings,
            'info': self.info,
            'summary': summary
        }

    def generate_report(self, results: Dict) -> str:
        """
        Generate human-readable report

        Args:
            results: Output from check_consistency()

        Returns:
            Formatted text report
        """
        lines = []
        lines.append("=" * 70)
        lines.append("MCNP LIBRARY CONSISTENCY CHECK")
        lines.append("=" * 70)
        lines.append("")

        # Summary
        summary = results['summary']
        lines.append("SUMMARY:")
        lines.append(f"  Library versions found: {summary['version_count']}")
        lines.append(f"  Consistency: {'✓ PASS' if summary['is_consistent'] else '⚠ WARNING - Mixed versions'}")
        lines.append("")

        # Version details
        lines.append("VERSION BREAKDOWN:")
        for version, info in summary['versions_used'].items():
            lines.append(f"  • {info['endf_name']} (.{version}c)")
            lines.append(f"    - Materials: {info['material_count']}")
            lines.append(f"    - Isotopes: {info['isotope_count']}")
        lines.append("")

        # Warnings
        if results['warnings']:
            lines.append("WARNINGS:")
            for warning in results['warnings']:
                lines.append(f"  ⚠ {warning['type']}")
                lines.append(f"    {warning['message']}")
                if 'recommendation' in warning:
                    lines.append(f"    Recommendation: {warning['recommendation']}")
                if 'versions' in warning:
                    lines.append("")
                    lines.append("    Version Details:")
                    for v in warning['versions']:
                        lines.append(f"      • {v['endf_name']}: {v['material_count']} materials")
                        if v['materials']:
                            mats = ', '.join([f"m{m}" for m in v['materials'][:5]])
                            if len(v['materials']) > 5:
                                mats += f"... (+{len(v['materials']) - 5} more)"
                            lines.append(f"        Materials: {mats}")
                lines.append("")

        # Info
        if results['info']:
            lines.append("INFO:")
            for info in results['info']:
                lines.append(f"  ✓ {info['message']}")
            lines.append("")

        lines.append("=" * 70)

        return '\n'.join(lines)


# Example usage and test cases
if __name__ == "__main__":
    checker = LibraryConsistencyChecker()

    # Test 1: Mixed library versions (AGR-1 pattern)
    print("Test 1: Mixed Library Versions (AGR-1 Pattern)")
    print("=" * 70)

    materials = {
        '2106': {  # ATR fuel - ENDF/B-VII.0
            '1001.70c': 3.393340E-02,
            '8016.70c': 1.696670E-02,
            '92235.70c': 4.198373E-04,
            '92238.70c': 3.775536E-03,
        },
        '9000': {  # SS316L - ENDF/B-VI.0
            '24050.00c': 0.00653131,
            '26056.00c': 0.60409084,
            '28058.00c': 0.08053185,
        },
        '8900': {  # Air - ENDF/B-VIII.0
            '7014.80c': 0.76,
            '8016.80c': 0.24,
        }
    }

    result = checker.check_consistency(materials)
    print(checker.generate_report(result))
    print("")

    # Test 2: Consistent library version
    print("Test 2: Consistent Library Version")
    print("=" * 70)

    materials_consistent = {
        '1': {
            '92235.80c': 0.045,
            '92238.80c': 0.955,
            '8016.80c': 2.0,
        },
        '2': {
            '1001.80c': 2.0,
            '8016.80c': 1.0,
        },
        '3': {
            '40000.80c': 1.0,
        }
    }

    result2 = checker.check_consistency(materials_consistent)
    print(checker.generate_report(result2))
    print("")

    # Test 3: Many mixed versions
    print("Test 3: Many Mixed Versions")
    print("=" * 70)

    materials_many = {
        '1': {'92235.80c': 1.0},  # ENDF/B-VIII.0
        '2': {'92235.71c': 1.0},  # ENDF/B-VII.1
        '3': {'92235.70c': 1.0},  # ENDF/B-VII.0
        '4': {'92235.60c': 1.0},  # ENDF/B-VI.8
        '5': {'92235.00c': 1.0},  # ENDF/B-VI.0
    }

    result3 = checker.check_consistency(materials_many)
    print(checker.generate_report(result3))

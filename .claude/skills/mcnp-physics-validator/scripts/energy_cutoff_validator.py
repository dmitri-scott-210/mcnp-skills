"""
MCNP Energy Cutoff and Range Validator

Validates energy cutoffs and ranges for different particle types and problem types.
Ensures PHYS card emax covers source energy and cutoffs are appropriate.
"""

from typing import Dict, List, Optional

class EnergyCutoffValidator:
    """Validate energy cutoffs and ranges in MCNP physics setup"""

    # Default cutoffs (MeV) per MCNP manual Table 4.3
    DEFAULT_CUTOFFS = {
        'N': {  # Neutron
            'lower': 0.0,
            'upper': 100.0,
            'description': 'Neutron energy cutoffs'
        },
        'P': {  # Photon
            'lower': 0.001,  # 1 keV
            'upper': 100.0,
            'description': 'Photon energy cutoffs'
        },
        'E': {  # Electron
            'lower': 0.001,  # 1 keV
            'upper': 100.0,
            'description': 'Electron energy cutoffs'
        },
        'H': {  # Proton
            'lower': 1.0,  # 1 MeV
            'upper': 100.0,
            'description': 'Proton energy cutoffs'
        }
    }

    # Recommended cutoffs for different problem types
    PROBLEM_TYPE_RECOMMENDATIONS = {
        'thermal_reactor': {
            'N': {'lower': 0.0, 'upper': 20.0, 'reason': 'Thermal neutrons important'},
            'P': {'lower': 0.0001, 'upper': 20.0, 'reason': 'Low-energy gammas important'},
        },
        'fast_reactor': {
            'N': {'lower': 1e-7, 'upper': 20.0, 'reason': 'Some thermal feedback'},
            'P': {'lower': 0.001, 'upper': 20.0, 'reason': 'Standard photon cutoff'},
        },
        'shielding': {
            'N': {'lower': 1e-8, 'upper': 20.0, 'reason': 'Deep penetration needs low cutoff'},
            'P': {'lower': 0.01, 'upper': 20.0, 'reason': 'Standard shielding cutoff'},
        },
        'fusion': {
            'N': {'lower': 0.0, 'upper': 20.0, 'reason': '14 MeV neutrons'},
            'P': {'lower': 0.001, 'upper': 20.0, 'reason': 'High-energy photons'},
        },
        'medical': {
            'N': {'lower': 0.0, 'upper': 20.0, 'reason': 'Thermal neutrons in BNCT'},
            'P': {'lower': 0.01, 'upper': 20.0, 'reason': 'Diagnostic/therapeutic energies'},
            'E': {'lower': 0.001, 'upper': 20.0, 'reason': 'Electron therapy'},
        },
    }

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def validate(self, mode: str, phys_cards: Dict, cut_cards: Dict,
                 source_energy: Optional[float] = None,
                 problem_type: Optional[str] = None) -> Dict:
        """
        Main validation method

        Args:
            mode: MODE card string (e.g., 'N P')
            phys_cards: {'PHYS:N': {...}, 'PHYS:P': {...}}
            cut_cards: {'CUT:N': {'lower': ..., 'upper': ...}, ...}
            source_energy: Maximum source energy in MeV (optional)
            problem_type: Type of problem for recommendations (optional)

        Returns:
            {'errors': [...], 'warnings': [...], 'info': [...]}
        """
        self.errors = []
        self.warnings = []
        self.info = []

        particles = self._parse_mode(mode)

        for particle in particles:
            self._validate_particle_cutoffs(particle, phys_cards, cut_cards,
                                           source_energy, problem_type)

        return self._format_results()

    def _parse_mode(self, mode: str) -> List[str]:
        """Parse MODE card to extract particle types"""
        # Extract particle designators (N, P, E, H, etc.)
        particles = []
        for char in mode.upper():
            if char in ['N', 'P', 'E', 'H', 'A', 'L', 'D', 'T', 'S', 'C', 'B', 'G', 'Z', 'F']:
                particles.append(char)
        return particles

    def _validate_particle_cutoffs(self, particle: str, phys_cards: Dict,
                                   cut_cards: Dict, source_energy: Optional[float],
                                   problem_type: Optional[str]):
        """Validate cutoffs for a specific particle type"""

        # Get PHYS card for this particle
        phys_key = f'PHYS:{particle}'
        phys = phys_cards.get(phys_key, {})

        # Get CUT card for this particle
        cut_key = f'CUT:{particle}'
        cut = cut_cards.get(cut_key, {})

        # Extract energy limits
        emax = phys.get('emax', self.DEFAULT_CUTOFFS.get(particle, {}).get('upper', 100.0))
        lower_cutoff = cut.get('lower', self.DEFAULT_CUTOFFS.get(particle, {}).get('lower', 0.0))

        # Validate emax vs source energy
        if source_energy and particle == 'N':
            if source_energy > emax:
                self.errors.append({
                    'type': 'SOURCE_EXCEEDS_EMAX',
                    'particle': particle,
                    'severity': 'ERROR',
                    'source_energy': source_energy,
                    'emax': emax,
                    'message': f'Source energy {source_energy} MeV exceeds PHYS:{particle} emax {emax} MeV',
                    'fix': f'Increase PHYS:{particle} emax to at least {source_energy * 1.1:.1f} MeV',
                    'impact': 'Particles above emax will not be transported correctly'
                })
            elif source_energy > emax * 0.9:
                self.warnings.append({
                    'type': 'SOURCE_NEAR_EMAX',
                    'particle': particle,
                    'severity': 'WARNING',
                    'source_energy': source_energy,
                    'emax': emax,
                    'message': f'Source energy {source_energy} MeV is close to PHYS:{particle} emax {emax} MeV',
                    'recommendation': f'Consider increasing emax to {source_energy * 1.5:.1f} MeV for safety margin'
                })

        # Validate cutoffs for problem type
        if problem_type and problem_type.lower() in self.PROBLEM_TYPE_RECOMMENDATIONS:
            rec = self.PROBLEM_TYPE_RECOMMENDATIONS[problem_type.lower()].get(particle)
            if rec:
                if lower_cutoff > rec['lower']:
                    self.warnings.append({
                        'type': 'CUTOFF_TOO_HIGH_FOR_PROBLEM',
                        'particle': particle,
                        'severity': 'WARNING',
                        'current_cutoff': lower_cutoff,
                        'recommended_cutoff': rec['lower'],
                        'problem_type': problem_type,
                        'message': f'{particle} lower cutoff {lower_cutoff} MeV may be too high for {problem_type}',
                        'reason': rec['reason'],
                        'recommendation': f'Consider CUT:{particle} J J -{rec["lower"]}'
                    })

        # Thermal reactor specific checks
        if problem_type and problem_type.lower() == 'thermal_reactor':
            if particle == 'N' and lower_cutoff > 1e-8:
                self.warnings.append({
                    'type': 'THERMAL_REACTOR_CUTOFF_WARNING',
                    'particle': particle,
                    'severity': 'WARNING',
                    'current_cutoff': lower_cutoff,
                    'message': 'Thermal reactor should typically use default neutron cutoff (0.0 MeV)',
                    'impact': 'May miss important thermal neutron interactions',
                    'recommendation': 'Use default cutoff (omit CUT:N or use CUT:N J J -0.0)'
                })

            if particle == 'P' and lower_cutoff > 0.0001:
                self.info.append({
                    'type': 'PHOTON_CUTOFF_SUGGESTION',
                    'particle': particle,
                    'current_cutoff': lower_cutoff,
                    'message': f'Current photon cutoff is {lower_cutoff} MeV ({lower_cutoff*1000:.1f} keV)',
                    'suggestion': 'For more accurate thermal reactor calculations, consider 100 eV cutoff',
                    'note': 'Lower cutoff increases runtime but improves accuracy',
                    'optional': True
                })

    def _format_results(self) -> Dict:
        """Format validation results"""
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'summary': {
                'errors': len(self.errors),
                'warnings': len(self.warnings),
                'passed': len(self.errors) == 0
            }
        }

    def generate_recommendations(self, problem_type: str, particles: List[str]) -> str:
        """
        Generate cutoff recommendations for problem type

        Args:
            problem_type: 'thermal_reactor', 'fast_reactor', etc.
            particles: List of particles ['N', 'P', ...]

        Returns:
            Formatted recommendation text
        """
        lines = []
        lines.append(f"RECOMMENDED CUTOFFS FOR {problem_type.upper()}")
        lines.append("=" * 70)

        if problem_type.lower() in self.PROBLEM_TYPE_RECOMMENDATIONS:
            recs = self.PROBLEM_TYPE_RECOMMENDATIONS[problem_type.lower()]

            for particle in particles:
                if particle in recs:
                    rec = recs[particle]
                    lines.append(f"\n{particle} (Neutron)" if particle == 'N' else f"\n{particle} (Photon)" if particle == 'P' else f"\n{particle}")
                    lines.append(f"  Lower cutoff: {rec['lower']} MeV")
                    lines.append(f"  Upper limit: {rec['upper']} MeV")
                    lines.append(f"  Reason: {rec['reason']}")
                    lines.append(f"  MCNP card: CUT:{particle} J J -{rec['lower']}")
                    if particle in ['N', 'P', 'E']:
                        lines.append(f"  PHYS card: PHYS:{particle} {rec['upper']}")
        else:
            lines.append(f"\nNo specific recommendations available for '{problem_type}'")
            lines.append("Available problem types:")
            for pt in self.PROBLEM_TYPE_RECOMMENDATIONS.keys():
                lines.append(f"  - {pt}")

        return '\n'.join(lines)


# Example usage and test cases
if __name__ == "__main__":
    validator = EnergyCutoffValidator()

    # Test 1: Source energy exceeds emax (ERROR)
    print("Test 1: Source Energy Exceeds EMAX")
    print("=" * 70)

    phys_cards = {'PHYS:N': {'emax': 10.0}}
    cut_cards = {}
    result = validator.validate('N', phys_cards, cut_cards, source_energy=14.0)

    print(f"Errors: {result['summary']['errors']}")
    if result['errors']:
        for err in result['errors']:
            print(f"\n❌ {err['type']}")
            print(f"   {err['message']}")
            print(f"   Fix: {err['fix']}")
    print()

    # Test 2: Thermal reactor with high cutoff (WARNING)
    print("Test 2: Thermal Reactor with High Cutoff")
    print("=" * 70)

    phys_cards = {'PHYS:N': {'emax': 20.0}}
    cut_cards = {'CUT:N': {'lower': 1e-6}}  # Too high for thermal
    result = validator.validate('N P', phys_cards, cut_cards,
                               problem_type='thermal_reactor')

    print(f"Warnings: {result['summary']['warnings']}")
    if result['warnings']:
        for warn in result['warnings']:
            print(f"\n⚠ {warn['type']}")
            print(f"   {warn['message']}")
            if 'recommendation' in warn:
                print(f"   Recommendation: {warn['recommendation']}")
    print()

    # Test 3: Generate recommendations
    print("Test 3: Recommendations for HTGR")
    print("=" * 70)
    print(validator.generate_recommendations('thermal_reactor', ['N', 'P']))
    print()

    # Test 4: All problem types
    print("Test 4: Recommendations for Different Problem Types")
    print("=" * 70)
    for problem_type in ['thermal_reactor', 'fast_reactor', 'shielding', 'fusion']:
        print(f"\n{validator.generate_recommendations(problem_type, ['N', 'P'])}\n")

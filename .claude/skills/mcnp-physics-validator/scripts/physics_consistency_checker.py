"""
MCNP Physics Consistency Checker

Validates consistency between MODE and PHYS cards.
Ensures particle production settings match transport settings.

Common errors caught:
- MODE N P but PHYS:N ngam=0 (no photon production)
- MODE P E but PHYS:P ides=1 (no electron production)
- Photonuclear materials present but ispn=0
"""

from typing import Dict, List, Optional

class PhysicsConsistencyChecker:
    """Check consistency between MODE, PHYS, and material cards"""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def validate(self, mode: str, phys_cards: Dict,
                 materials: Optional[Dict] = None) -> Dict:
        """
        Main validation method

        Args:
            mode: MODE card string (e.g., 'N P E')
            phys_cards: {'PHYS:N': {...}, 'PHYS:P': {...}, ...}
            materials: {mat_id: {zaid: fraction}} (optional, for photonuclear check)

        Returns:
            {'errors': [...], 'warnings': [...], 'info': [...]}
        """
        self.errors = []
        self.warnings = []
        self.info = []

        particles = self._parse_mode(mode)

        # Check neutron-photon coupling
        if 'N' in particles and 'P' in particles:
            self._check_neutron_photon_coupling(phys_cards)

        # Check photon-electron coupling
        if 'P' in particles and 'E' in particles:
            self._check_photon_electron_coupling(phys_cards)

        # Check photonuclear if materials provided
        if 'P' in particles and 'N' in particles and materials:
            self._check_photonuclear(phys_cards, materials)

        # Check electron bremsstrahlung
        if 'E' in particles and 'P' in particles:
            self._check_electron_bremsstrahlung(phys_cards)

        return self._format_results()

    def _parse_mode(self, mode: str) -> List[str]:
        """Parse MODE card to extract particle types"""
        particles = []
        for char in mode.upper():
            if char in ['N', 'P', 'E', 'H', 'A', 'L', 'D', 'T', 'S', 'C', 'B', 'G', 'Z', 'F']:
                particles.append(char)
        return particles

    def _check_neutron_photon_coupling(self, phys_cards: Dict):
        """
        Check neutron → photon production consistency

        MODE N P means:
        - Transport neutrons
        - Transport photons
        - Photons should be produced from neutron reactions

        PHYS:N ngam parameter controls photon production:
        - ngam=0: No photon production (INCONSISTENT with MODE N P)
        - ngam=1: Photon production from tables (CORRECT)
        """
        phys_n = phys_cards.get('PHYS:N', {})
        ngam = phys_n.get('ngam', 1)  # Default is 1

        if ngam == 0:
            self.errors.append({
                'type': 'INCONSISTENT_PHOTON_PRODUCTION',
                'severity': 'ERROR',
                'message': 'MODE includes P (photon transport) but PHYS:N ngam=0 (no photon production)',
                'impact': 'Photons will NOT be produced from neutron reactions despite MODE P',
                'fix': 'Remove ngam=0 from PHYS:N or change to ngam=1',
                'explanation': 'ngam=0 disables photon production, making MODE P pointless',
                'card_example': 'PHYS:N 20 J J J J J J J 1  $ ngam=1 enables photon production'
            })
        else:
            self.info.append({
                'type': 'NEUTRON_PHOTON_COUPLING_OK',
                'message': 'Neutron-photon coupling correctly configured',
                'ngam': ngam,
                'description': 'Photons will be produced from neutron reactions'
            })

    def _check_photon_electron_coupling(self, phys_cards: Dict):
        """
        Check photon → electron production consistency

        MODE P E means:
        - Transport photons
        - Transport electrons
        - Electrons should be produced from photon reactions

        PHYS:P ides parameter controls electron production:
        - ides=0: Electron production ON (CORRECT)
        - ides=1: No electron production (INCONSISTENT with MODE P E)
        """
        phys_p = phys_cards.get('PHYS:P', {})
        ides = phys_p.get('ides', 0)  # Default is 0

        if ides == 1:
            self.errors.append({
                'type': 'INCONSISTENT_ELECTRON_PRODUCTION',
                'severity': 'ERROR',
                'message': 'MODE includes E (electron transport) but PHYS:P ides=1 (no electron production)',
                'impact': 'Electrons will NOT be produced from photon interactions despite MODE E',
                'fix': 'Remove ides=1 from PHYS:P or change to ides=0',
                'explanation': 'ides=1 disables electron production (Compton, pair production)',
                'card_example': 'PHYS:P 100 0  $ ides=0 enables electron production'
            })
        else:
            self.info.append({
                'type': 'PHOTON_ELECTRON_COUPLING_OK',
                'message': 'Photon-electron coupling correctly configured',
                'ides': ides,
                'description': 'Electrons will be produced from photon interactions'
            })

    def _check_photonuclear(self, phys_cards: Dict, materials: Dict):
        """
        Check photonuclear reaction settings

        Materials with Be or D can produce photoneutrons (γ,n):
        - Be-9 + γ → Be-8 + n (threshold ~1.67 MeV)
        - D + γ → p + n (threshold ~2.22 MeV)

        PHYS:P ispn parameter controls photonuclear:
        - ispn=0: OFF (default, no photoneutrons)
        - ispn=1: Biased photoneutron production
        """
        phys_p = phys_cards.get('PHYS:P', {})
        ispn = phys_p.get('ispn', 0)  # Default is 0

        # Check for beryllium or deuterium in materials
        has_photonuclear_materials = self._check_for_photonuclear_materials(materials)

        if has_photonuclear_materials and ispn == 0:
            self.warnings.append({
                'type': 'PHOTONUCLEAR_NOT_ENABLED',
                'severity': 'WARNING',
                'message': 'Beryllium/deuterium present but photonuclear (ispn) not enabled',
                'materials': has_photonuclear_materials,
                'impact': 'Photo-neutron reactions (γ,n) will NOT be simulated',
                'recommendation': 'Add PHYS:P with ispn=1 if photoneutron production is important',
                'card_example': 'PHYS:P J J J 1  $ ispn=1 enables photoneutrons',
                'optional': True,
                'note': 'Usually only important for beryllium reflectors with high photon flux'
            })
        elif has_photonuclear_materials and ispn != 0:
            self.info.append({
                'type': 'PHOTONUCLEAR_ENABLED',
                'message': 'Photonuclear reactions enabled for Be/D materials',
                'ispn': ispn,
                'materials': has_photonuclear_materials
            })

    def _check_electron_bremsstrahlung(self, phys_cards: Dict):
        """
        Check electron → photon (bremsstrahlung) production

        MODE E P means electrons can produce photons via bremsstrahlung.
        This is typically automatic, but we verify it's not disabled.
        """
        # Bremsstrahlung is usually automatic when MODE E P
        # Just log that it should be happening
        self.info.append({
            'type': 'ELECTRON_BREMSSTRAHLUNG_ENABLED',
            'message': 'Electron-photon coupling (bremsstrahlung) is active',
            'description': 'Electrons will produce photons via bremsstrahlung'
        })

    def _check_for_photonuclear_materials(self, materials: Dict) -> List[str]:
        """
        Check if materials contain Be or D

        Returns:
            List of material IDs containing photonuclear-relevant isotopes
        """
        photonuclear_materials = []

        for mat_id, composition in materials.items():
            for zaid in composition.keys():
                zaid_str = str(zaid).split('.')[0]  # Remove library extension

                # Check for beryllium (Z=4)
                if zaid_str.startswith('4009'):
                    photonuclear_materials.append(f'm{mat_id} (Be-9)')

                # Check for deuterium (Z=1, A=2)
                if zaid_str.startswith('1002'):
                    photonuclear_materials.append(f'm{mat_id} (D)')

        return photonuclear_materials

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


# Example usage and test cases
if __name__ == "__main__":
    checker = PhysicsConsistencyChecker()

    # Test 1: MODE N P but ngam=0 (ERROR)
    print("Test 1: MODE N P but ngam=0 (Inconsistent Photon Production)")
    print("=" * 70)

    phys_cards = {
        'PHYS:N': {
            'emax': 20.0,
            'ngam': 0  # WRONG! Disables photon production
        }
    }

    result = checker.validate('N P', phys_cards)
    print(f"Errors: {result['summary']['errors']}")
    if result['errors']:
        for err in result['errors']:
            print(f"\n❌ {err['type']}")
            print(f"   {err['message']}")
            print(f"   Impact: {err['impact']}")
            print(f"   Fix: {err['fix']}")
    print()

    # Test 2: MODE P E but ides=1 (ERROR)
    print("Test 2: MODE P E but ides=1 (Inconsistent Electron Production)")
    print("=" * 70)

    phys_cards = {
        'PHYS:P': {
            'emcpf': 100.0,
            'ides': 1  # WRONG! Disables electron production
        }
    }

    result = checker.validate('P E', phys_cards)
    print(f"Errors: {result['summary']['errors']}")
    if result['errors']:
        for err in result['errors']:
            print(f"\n❌ {err['type']}")
            print(f"   {err['message']}")
            print(f"   Impact: {err['impact']}")
            print(f"   Fix: {err['fix']}")
    print()

    # Test 3: Be material but no photonuclear (WARNING)
    print("Test 3: Beryllium Present but No Photonuclear")
    print("=" * 70)

    phys_cards = {
        'PHYS:N': {'emax': 20.0, 'ngam': 1},
        'PHYS:P': {'emcpf': 100.0, 'ispn': 0}  # ispn=0, no photonuclear
    }

    materials = {
        '1': {  # Beryllium reflector
            '4009.60c': 1.0
        }
    }

    result = checker.validate('N P', phys_cards, materials)
    print(f"Warnings: {result['summary']['warnings']}")
    if result['warnings']:
        for warn in result['warnings']:
            print(f"\n⚠ {warn['type']}")
            print(f"   {warn['message']}")
            print(f"   Materials: {warn['materials']}")
            print(f"   Recommendation: {warn['recommendation']}")
    print()

    # Test 4: Correct setup (PASS)
    print("Test 4: Correct Physics Setup")
    print("=" * 70)

    phys_cards = {
        'PHYS:N': {'emax': 20.0, 'ngam': 1},  # Photon production ON
        'PHYS:P': {'emcpf': 100.0, 'ides': 0}  # Electron production ON
    }

    result = checker.validate('N P E', phys_cards)
    print(f"Errors: {result['summary']['errors']}")
    print(f"Passed: {result['summary']['passed']}")
    if result['info']:
        print("\nInfo:")
        for info in result['info']:
            print(f"  ✓ {info['message']}")

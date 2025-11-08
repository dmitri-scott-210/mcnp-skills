"""
MCNP Burnup Builder (Skill 22) - MCNP-ORIGEN/CINDER coupling for depletion

Based on MCNP6 Burnup Capabilities:
- BURN card: Depletes materials over time
- Tracks isotopic composition changes
- Calculates decay heat, activity, dose
- Requires CINDER-90 or ORIGEN libraries
- Not available in all MCNP6 distributions

NOTE: Burnup capability availability varies by MCNP6 version and installation.
Check your MCNP6 manual for specific BURN card format and keywords.

References:
- COMPLETE_MCNP6_KNOWLEDGE_BASE.md: ADVANCED OPERATIONS section
- MCNP6 User Manual Chapter 5 (if BURN available)
- LA-UR-17-29981 (MCNP6.2 Release Notes)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from typing import List, Dict, Optional

class MCNPBurnupBuilder:
    """
    Build MCNP burnup/depletion specifications

    NOTE: BURN card syntax varies by MCNP version. This implementation
    provides a general framework - verify against your MCNP6 manual.

    Capabilities:
    - Material depletion specification
    - Burnup time steps
    - Power level specifications
    - Depletion cell tracking
    """

    def __init__(self):
        self.burn_cards = []
        self.depletion_cells = []
        self.materials_to_deplete = {}

    def add_burn_specification(self, material: int, power_mw: float,
                              burnup_steps: List[float], units: str = 'days') -> str:
        """
        Add burnup specification for material

        Args:
            material: Material number to deplete
            power_mw: Power level in megawatts
            burnup_steps: List of time steps
            units: Time units ('days', 'years', 'seconds')

        Returns:
            BURN card string (format varies by MCNP version)

        NOTE: Actual BURN card format depends on your MCNP6 version.
        Common formats:
            BURN MAT=m POWER=p TIME=t1 t2 t3 ...
            BURN m p t1 t2 t3 ...
        """
        # Store material depletion info
        self.materials_to_deplete[material] = {
            'power_mw': power_mw,
            'steps': burnup_steps,
            'units': units
        }

        # Generate BURN card (generic format - adjust for your MCNP version)
        card = f"burn mat={material} power={power_mw}"
        card += f" time=" + " ".join(map(str, burnup_steps))
        card += f"  $ {units}"

        self.burn_cards.append(card)
        return card

    def set_depletion_cells(self, cells: List[int]) -> None:
        """
        Specify cells for depletion tracking

        Args:
            cells: List of cell numbers where depletion occurs
        """
        self.depletion_cells = cells

    def calculate_burnup_mwd_kghm(self, power_mw: float, mass_kghm: float,
                                   time_days: float) -> float:
        """
        Calculate burnup in MWd/kgHM

        Args:
            power_mw: Power in megawatts
            mass_kghm: Mass of heavy metal in kg
            time_days: Burnup time in days

        Returns:
            Burnup in MWd/kgHM
        """
        burnup = (power_mw * time_days) / mass_kghm
        return burnup

    def estimate_depletion_runtime(self, n_steps: int, particles_per_step: int,
                                   step_time_sec: float = 60.0) -> Dict[str, float]:
        """
        Estimate total runtime for depletion calculation

        Args:
            n_steps: Number of burnup steps
            particles_per_step: Particles per depletion step
            step_time_sec: Estimated time per step in seconds

        Returns:
            Dict with runtime estimates
        """
        total_steps = n_steps
        total_particles = n_steps * particles_per_step
        estimated_time_hours = (n_steps * step_time_sec) / 3600.0

        return {
            'total_steps': total_steps,
            'total_particles': total_particles,
            'estimated_hours': estimated_time_hours,
            'recommendation': f"Burnup calculation: {n_steps} steps, ~{estimated_time_hours:.1f} hours"
        }

    def generate_depletion_info(self) -> str:
        """
        Generate informational output about depletion setup

        Returns:
            Multi-line string with depletion configuration
        """
        info = ["Burnup/Depletion Configuration:"]
        info.append("")

        for mat, config in self.materials_to_deplete.items():
            info.append(f"Material {mat}:")
            info.append(f"  Power: {config['power_mw']} MW")
            info.append(f"  Steps: {len(config['steps'])} ({config['units']})")
            info.append(f"  Time points: {config['steps']}")
            info.append("")

        if self.depletion_cells:
            info.append(f"Depletion cells: {self.depletion_cells}")

        info.append("")
        info.append("NOTE: Verify BURN card format against your MCNP6 manual.")
        info.append("      Burnup capability may not be available in all distributions.")

        return "\n".join(info)

    def generate_cards(self) -> str:
        """Generate all burnup/depletion cards"""
        if not self.burn_cards:
            return "c No burnup cards defined"

        lines = ["c Burnup/Depletion Cards"]
        lines.append("c NOTE: BURN card format varies by MCNP6 version")
        lines.append("c       Verify syntax against your MCNP6 manual")
        lines.extend(self.burn_cards)
        return "\n".join(lines)

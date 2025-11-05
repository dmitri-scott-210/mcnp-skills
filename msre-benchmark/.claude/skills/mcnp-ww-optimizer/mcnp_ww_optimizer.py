"""
MCNP Weight Window Optimizer (Skill 25) - Weight window generation and optimization

Based on MCNP6.3 Chapter 5.12 - Variance Reduction:
- WWG card: Generates weight windows from tally results
- WWN/WWE/WWT: Weight window bounds by cell, energy, and time
- WWP: Weight window parameters (cutoff, survival, max split)
- MESH card: Superimposed mesh for mesh-based weight windows
- Iterative optimization: 2-3 iterations for convergence

Methods:
- MAGIC (default): Track-length estimator from tally
- Importance-based: Uses adjoint flux
- Mesh-based: Superimposed MESH for complex geometries

References:
- COMPLETE_MCNP6_KNOWLEDGE_BASE.md: ADVANCED OPERATIONS section
- Chapter 5.12: Variance Reduction Cards
- Chapter 2.7: Variance Reduction Theory
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from typing import List, Dict, Tuple, Optional

class MCNPWeightWindowOptimizer:
    """
    Optimize MCNP variance reduction with weight windows

    Capabilities:
    - WWG-based generation from tally
    - Mesh-based weight windows
    - Iterative optimization workflow
    - WWP parameter tuning
    """

    def __init__(self):
        self.ww_cards = []
        self.wwp_params = {}
        self.mesh_defined = False

    def setup_wwg(self, tally_num: int, particle: str = 'n',
                  update_factor: float = 0.5, softening: float = 0.5,
                  min_ratio: Optional[float] = None,
                  max_ratio: Optional[float] = None) -> str:
        """
        Set up weight window generator from tally

        Args:
            tally_num: Tally number for WW generation
            particle: Particle type (n, p)
            update_factor: wg1 = fraction of new WW (default 0.5 = 50%/50% mix)
            softening: wg2 = softening factor (default 0.5)
            min_ratio: wg3 = minimum WW ratio allowed
            max_ratio: wg4 = maximum WW ratio allowed

        Returns:
            WWG card string

        Format: WWG n wg1 wg2 wg3 wg4 wg5 wg6 wg7 wg8
        """
        card = f"wwg:{particle} {tally_num}"

        # Add control parameters if specified
        params = []
        if update_factor != 0.5:
            params.append(str(update_factor))
        if softening != 0.5:
            while len(params) < 1:
                params.append("0.5")  # Fill defaults
            params.append(str(softening))
        if min_ratio is not None:
            while len(params) < 2:
                params.append("j")  # Use default
            params.append(str(min_ratio))
        if max_ratio is not None:
            while len(params) < 3:
                params.append("j")
            params.append(str(max_ratio))

        if params:
            card += " " + " ".join(params)

        self.ww_cards.append(card)
        return card

    def add_wwn_bounds(self, particle: str, lower_bounds: List[float]) -> str:
        """
        Add weight window lower bounds by cell

        Args:
            particle: Particle type
            lower_bounds: Lower WW bound for each cell

        Returns:
            WWN card string
        """
        card = f"wwn:{particle} " + " ".join(map(str, lower_bounds))
        self.ww_cards.append(card)
        return card

    def add_wwe_energy_bins(self, particle: str, energy_bins: List[float]) -> str:
        """
        Add energy bins for weight windows

        Args:
            particle: Particle type
            energy_bins: Energy boundaries (K+1 values for K bins)

        Returns:
            WWE card string
        """
        card = f"wwe:{particle} " + " ".join(map(str, energy_bins))
        self.ww_cards.append(card)
        return card

    def add_wwp_parameters(self, particle: str, weight_cutoff: float = 0.25,
                          weight_survival: float = 0.5, max_split: int = 5,
                          rr_energy: float = 0.0) -> str:
        """
        Add weight window parameters

        Args:
            particle: Particle type
            weight_cutoff: wc1 = below this weight, Russian roulette (default 0.25)
            weight_survival: wc2 = survival weight for RR (default 0.5)
            max_split: wc3 = maximum split factor (default 5)
            rr_energy: we = Russian roulette energy threshold (default 0)

        Returns:
            WWP card string
        """
        card = f"wwp:{particle} {weight_cutoff} {weight_survival} {max_split} {rr_energy}"
        self.ww_cards.append(card)
        self.wwp_params[particle] = {
            'cutoff': weight_cutoff,
            'survival': weight_survival,
            'max_split': max_split,
            'rr_energy': rr_energy
        }
        return card

    def add_mesh_for_ww(self, particle: str, mesh_type: str, origin: Tuple[float, float, float],
                       imesh: List[float], jmesh: List[float], kmesh: List[float],
                       iints: List[int], jints: List[int], kints: List[int]) -> str:
        """
        Add superimposed mesh for mesh-based weight windows

        Args:
            particle: Particle type
            mesh_type: 'xyz' (rectangular) or 'cyl' (cylindrical)
            origin: (x, y, z) mesh origin
            imesh, jmesh, kmesh: Mesh boundaries
            iints, jints, kints: Intervals between boundaries

        Returns:
            MESH card string (used with WWG)
        """
        card = f"mesh geom={mesh_type} origin={origin[0]} {origin[1]} {origin[2]}"
        card += f" imesh=" + " ".join(map(str, imesh))
        card += f" iints=" + " ".join(map(str, iints))
        card += f" jmesh=" + " ".join(map(str, jmesh))
        card += f" jints=" + " ".join(map(str, jints))
        card += f" kmesh=" + " ".join(map(str, kmesh))
        card += f" kints=" + " ".join(map(str, kints))

        self.ww_cards.append(card)
        self.mesh_defined = True
        return card

    def generate_optimization_workflow(self, n_iterations: int = 3,
                                      particles_per_iteration: int = 1000000) -> str:
        """
        Generate iterative weight window optimization workflow

        Procedure:
        1. Run base problem to generate initial WW
        2. Run with WW, update WW from results
        3. Repeat 2-3 times for convergence

        Args:
            n_iterations: Number of optimization iterations (default 3)
            particles_per_iteration: Particles per iteration

        Returns:
            Workflow instructions
        """
        workflow = f"""
Weight Window Optimization Workflow ({n_iterations} iterations):

Iteration 1 (Generate Initial WW):
  - Run with WWG card only (no WWN/WWE)
  - MCNP generates initial weight windows
  - Output: WWINP file with weight windows

Iterations 2-{n_iterations} (Refine WW):
  - Copy WWINP to INPUT or use FILES card
  - Run with existing WW + WWG for update
  - MCNP refines weight windows
  - Check FOM improvement

Convergence Criteria:
  - FOM stable (variation <10%)
  - Relative error meets target
  - WW ratios reasonable (<100)

Recommended NPS: {particles_per_iteration:,} per iteration
Total particles: {n_iterations * particles_per_iteration:,}
"""
        return workflow

    def check_ww_quality(self, ww_ratios: List[float]) -> Dict[str, any]:
        """
        Check weight window quality metrics

        Args:
            ww_ratios: Ratios of max/min WW in each region

        Returns:
            Quality assessment dict
        """
        max_ratio = max(ww_ratios)
        avg_ratio = sum(ww_ratios) / len(ww_ratios)

        quality = {
            'max_ratio': max_ratio,
            'avg_ratio': avg_ratio,
            'status': 'good' if max_ratio < 10 else 'acceptable' if max_ratio < 100 else 'poor',
            'recommendation': ''
        }

        if max_ratio > 100:
            quality['recommendation'] = "WW ratios too large - increase mesh resolution or reduce perturbation"
        elif max_ratio > 50:
            quality['recommendation'] = "WW ratios high - consider additional iteration"
        else:
            quality['recommendation'] = "WW quality good - ready for production"

        return quality

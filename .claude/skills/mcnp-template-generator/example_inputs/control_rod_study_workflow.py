"""
Control Rod Worth Curve Workflow
Generate 11 configurations for rod positions 0% to 100% withdrawn
"""

from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import numpy as np
import os


# Configuration
POSITIONS = np.arange(0, 101, 10)  # 0, 10, 20, ..., 100 percent withdrawn
ROD_HEIGHT = 100.0  # cm


def generate_control_rod_geometry(position_pct, rod_height=100):
    """
    Generate control rod cell definition.
    
    Args:
        position_pct: 0-100% withdrawn
        rod_height: Total rod height (cm)
    """
    withdrawn_height = rod_height * position_pct / 100.0
    inserted_height = rod_height - withdrawn_height
    
    cells = f"""c Control rod at {position_pct}% withdrawn ({inserted_height:.1f} cm inserted)
  100  10  -5.0    -100  -200  {inserted_height:.4f}    $ Poison section (inserted)
  101  20  -1.0    -100  -200  -{inserted_height:.4f}   $ Follower section (withdrawn)
"""
    
    return cells


def generate_inputs():
    """Generate control rod worth curve inputs."""
    
    print("=" * 70)
    print("Control Rod Worth Curve Study")
    print("=" * 70)
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'generated_rod_worth_study')
    os.makedirs(output_dir, exist_ok=True)
    
    # Create template
    template_content = """c Reactor Core - Control Rod at {{rod_position}}% Withdrawn
c Generated: {{generation_date}}
c Case ID: {{case_id}}
c
c BLOCK 1: CELL CARDS
c
c --- Fixed Core Cells ---
  1  1  -2.7   -10  100  -300          $ Core region
  2  2  -1.0   -20   10  100  -300     $ Moderator
c
c --- Variable Control Rod ---
{{control_rod_cells}}
c
  999  0         20                     $ Void outside
c
c --- End of Cell Block ---

c
c BLOCK 2: SURFACE CARDS
c
c --- Fixed Core Surfaces ---
  10  cz  50.0                          $ Core radius
  20  cz  70.0                          $ Tank radius
  100 pz  0.0                           $ Bottom
  200 pz  {{rod_height}}                $ Rod guide tube top
  300 pz  150.0                         $ Core top
c
c --- Control Rod Surfaces ---
  *100 cz  2.0                          $ Control rod radius
c
c --- End of Surface Block ---

c
c BLOCK 3: DATA CARDS
c
mode n
c
c --- Core Material ---
m1  $ UO2 fuel
   92235.70c  0.04
   92238.70c  0.96
    8016.70c  2.0
c
c --- Moderator ---
m2  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt2  lwtr.70t
c
c --- Control Rod Poison ---
m10  $ B4C
    5010.70c  0.8
    5011.70c  0.2
    6000.70c  1.0
c
c --- Rod Follower ---
m20  $ Stainless steel
   26000.70c  0.7
   24000.70c  0.2
   28000.70c  0.1
c
c --- Criticality Card ---
kcode 10000 1.0 50 250
ksrc  0 0 75
c
c --- Tallies ---
f4:n  1
e4    0.625e-6 20.0
nps 500000
"""
    
    # Write template
    template_path = os.path.join(output_dir, 'core_model.template')
    with open(template_path, 'w') as f:
        f.write(template_content)
    
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(output_dir))
    template = env.get_template('core_model.template')
    
    # Generate inputs for each rod position
    print(f"\nGenerating MCNP inputs in {output_dir}/...")
    print("-" * 70)
    
    for pos in POSITIONS:
        rod_geometry = generate_control_rod_geometry(pos, ROD_HEIGHT)
        case_id = f'rod_{pos:03d}'
        
        output = template.render(
            rod_position=pos,
            control_rod_cells=rod_geometry,
            case_id=case_id,
            rod_height=ROD_HEIGHT,
            generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        filename = os.path.join(output_dir, f'core_{case_id}.i')
        with open(filename, 'w') as f:
            f.write(output)
        
        print(f"✓ {pos:3d}% withdrawn: {filename}")
    
    print("-" * 70)
    print(f"\n✓ Generated {len(POSITIONS)} rod position cases")
    print(f"  Template: {template_path}")
    
    print("\nNext steps:")
    print(f"  1. Run MCNP for all positions")
    print(f"  2. Extract keff from output files")
    print(f"  3. Calculate differential rod worth: dk/k per % withdrawal")
    print(f"  4. Plot rod worth curve")


if __name__ == "__main__":
    generate_inputs()

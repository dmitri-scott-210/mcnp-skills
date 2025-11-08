"""
Enrichment Sensitivity Study Workflow
Parameter sweep from 3.0% to 5.0% enrichment in 0.5% steps
"""

from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os


# Configuration
ENRICHMENTS = [3.0, 3.5, 4.0, 4.5, 5.0]


def generate_uo2_material(enrichment_pct, material_num=1):
    """Generate UO2 fuel material card."""
    u235_frac = enrichment_pct / 100.0
    u238_frac = 1.0 - u235_frac
    
    return f"""m{material_num}  $ UO2 fuel, {enrichment_pct}% enriched
   92235.70c  {u235_frac:.6f}
   92238.70c  {u238_frac:.6f}
    8016.70c  2.0
mt{material_num}  u/o2.70t
"""


def generate_inputs():
    """Generate enrichment sensitivity study inputs."""
    
    print("=" * 70)
    print("Enrichment Sensitivity Study")
    print("=" * 70)
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'generated_enrichment_study')
    os.makedirs(output_dir, exist_ok=True)
    
    # Create template
    template_content = """c PWR Assembly - Enrichment {{enrichment}}%
c Generated: {{generation_date}}
c Case ID: {{case_id}}
c
c BLOCK 1: CELL CARDS
c
  1  1  -10.4   -10  100  -200          $ UO2 fuel pin
  2  2   -6.5   -20   10  100  -200     $ Zircaloy clad
  3  3   -1.0   -30   20  100  -200     $ Water moderator
c
c --- End of Cell Block ---

c
c BLOCK 2: SURFACE CARDS
c
  10  cz  0.4096                        $ Fuel radius
  20  cz  0.4750                        $ Clad outer radius
  30  cz  0.6350                        $ Pin pitch boundary
  100 pz  0.0                           $ Bottom
  200 pz  365.76                        $ Top
c
c --- End of Surface Block ---

c
c BLOCK 3: DATA CARDS
c
mode n
c
c --- Variable Fuel Material ---
{{fuel_material}}
c
c --- Clad Material ---
m2  $ Zircaloy-4
   40000.70c  0.98  
   26000.70c  0.02
c
c --- Moderator Material ---
m3  $ Water
    1001.70c  2.0
    8016.70c  1.0
mt3  lwtr.70t
c
c --- Criticality Card ---
kcode 10000 1.0 50 250
ksrc  0 0 182.88
c
c --- Tallies ---
f4:n  1
e4    0.625e-6 20.0
nps 500000
"""
    
    # Write template
    template_path = os.path.join(output_dir, 'pwr_assembly.template')
    with open(template_path, 'w') as f:
        f.write(template_content)
    
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(output_dir))
    template = env.get_template('pwr_assembly.template')
    
    # Generate inputs for each enrichment
    print(f"\nGenerating MCNP inputs in {output_dir}/...")
    print("-" * 70)
    
    for enr in ENRICHMENTS:
        fuel_material = generate_uo2_material(enr)
        case_id = f'enr{int(enr*10):02d}'
        
        output = template.render(
            enrichment=enr,
            fuel_material=fuel_material,
            case_id=case_id,
            generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        filename = os.path.join(output_dir, f'pwr_{case_id}.i')
        with open(filename, 'w') as f:
            f.write(output)
        
        print(f"✓ {enr:4.1f}%: {filename}")
    
    print("-" * 70)
    print(f"\n✓ Generated {len(ENRICHMENTS)} MCNP inputs")
    print(f"  Template: {template_path}")
    
    print("\nNext steps:")
    print(f"  1. Run MCNP for all cases")
    print(f"  2. Extract keff from output files")
    print(f"  3. Plot keff vs enrichment")


if __name__ == "__main__":
    generate_inputs()

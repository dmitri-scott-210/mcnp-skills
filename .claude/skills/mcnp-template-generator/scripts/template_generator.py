#!/usr/bin/env python3
"""
MCNP Template Generator

Generate MCNP input templates for common problem types.

Usage:
    python template_generator.py --type shielding --geometry sphere
    python template_generator.py  # Interactive mode
"""

import sys
import argparse

SHIELDING_SPHERE = """c ===================================================================
c TEMPLATE: Spherical Shielding Problem
c ===================================================================
c DESCRIPTION: Point isotropic source in center of spherical shield
c PARAMETERS TO CUSTOMIZE:
c   [SHIELD_RADIUS_CM] = Shield outer radius (cm)
c   [SOURCE_STRENGTH] = Source strength (particles/s)
c ===================================================================

c Cell Cards
1  1  -11.3  -1  IMP:N=1  $ Shield (lead, adjust material/density)
2  0        1    IMP:N=0  $ Void outside

c Surface Cards
1  SO  [SHIELD_RADIUS_CM]  $ Shield outer surface

c Data Cards
MODE  N
SDEF  POS=0 0 0  ERG=1.0  $ 1 MeV point source
M1  82000.80c  1.0  $ Lead (natural)
F2:N  1  $ Current at shield surface
F4:N  2  $ Flux beyond shield
NPS  1000000
"""

CRITICALITY_BARE = """c ===================================================================
c TEMPLATE: Bare Criticality Sphere
c ===================================================================
c DESCRIPTION: Bare fissile sphere for keff calculation
c PARAMETERS TO CUSTOMIZE:
c   [CORE_RADIUS_CM] = Core radius (cm)
c   [U235_DENSITY] = U-235 metal density (g/cm³)
c ===================================================================

c Cell Cards
1  1  -[U235_DENSITY]  -1  IMP:N=1  $ Fissile core
2  0   1  IMP:N=0  $ Void outside

c Surface Cards
1  SO  [CORE_RADIUS_CM]  $ Core outer surface

c Data Cards
MODE  N
KCODE  10000  1.0  50  250  $ 10K/cycle, skip 50, run 250
KSRC  0 0 0  $ Initial source at center
M1  92235.80c  1.0  $ U-235 metal
F4:N  1  $ Flux in core
F7:N  1  $ Fission rate in core
"""

DOSE_AMBIENT = """c ===================================================================
c TEMPLATE: Ambient Dose Equivalent H*(10)
c ===================================================================
c DESCRIPTION: Point source ambient dose calculation
c PARAMETERS TO CUSTOMIZE:
c   [DETECTOR_DISTANCE_CM] = Distance from source (cm)
c   [SOURCE_ENERGY_MEV] = Source energy (MeV)
c ===================================================================

c Cell Cards
1  0  -1  IMP:N=1  $ Void around source
2  0   1 -2  IMP:N=1  $ Detector region
3  0   2  IMP:N=0  $ Outside

c Surface Cards
1  SO  0.1  $ Small source region
2  SO  [DETECTOR_DISTANCE_CM]  $ Detector sphere

c Data Cards
MODE  N
SDEF  POS=0 0 0  ERG=[SOURCE_ENERGY_MEV]
F4:N  2  $ Flux at detector
FM4  -1.602E-10  $ Convert to dose (Sv)
DE4  0.01 0.1 1.0 10.0  $ Energy bins (MeV)
DF4  0.5 0.8 1.2 1.5  $ Dose conversion factors (example)
NPS  1000000
"""

TEMPLATES = {
    'shielding_sphere': SHIELDING_SPHERE,
    'criticality_bare': CRITICALITY_BARE,
    'dose_ambient': DOSE_AMBIENT
}

def generate_template(template_type, output_file):
    """Generate template"""
    
    key = f"{template_type}_sphere" if template_type in ['shielding', 'criticality'] else template_type
    
    if key not in TEMPLATES and template_type not in TEMPLATES:
        print(f"ERROR: Unknown template type '{template_type}'")
        print(f"Available: shielding, criticality, dose")
        return False
    
    template = TEMPLATES.get(key) or TEMPLATES.get(template_type)
    
    with open(output_file, 'w') as f:
        f.write(template)
    
    return True

def interactive_mode():
    """Interactive template generation"""
    print("=" * 60)
    print("MCNP Template Generator")
    print("=" * 60)
    
    print("\nAvailable templates:")
    print("  1. Shielding (sphere)")
    print("  2. Criticality (bare sphere)")
    print("  3. Dose (ambient H*10)")
    
    choice = input("\nSelect template (1-3): ").strip()
    
    template_map = {
        '1': 'shielding',
        '2': 'criticality',
        '3': 'dose'
    }
    
    if choice not in template_map:
        print("ERROR: Invalid choice")
        return
    
    template_type = template_map[choice]
    output_file = input(f"Output file [{template_type}.i]: ").strip() or f"{template_type}.i"
    
    if generate_template(template_type, output_file):
        print(f"\n✓ Created {output_file}")
        print(f"  Template type: {template_type}")
        print(f"\nNext steps:")
        print(f"  1. Edit {output_file} and replace [PARAMETER] values")
        print(f"  2. Run: mcnp6 inp={output_file}")

def main():
    parser = argparse.ArgumentParser(description='Generate MCNP input templates')
    parser.add_argument('--type', choices=['shielding', 'criticality', 'dose'], 
                       help='Template type')
    parser.add_argument('--geometry', default='sphere', help='Geometry type')
    parser.add_argument('--output', help='Output file')
    
    args = parser.parse_args()
    
    if not args.type:
        interactive_mode()
    else:
        output = args.output or f"{args.type}_{args.geometry}.i"
        if generate_template(args.type, output):
            print(f"Created {output}")

if __name__ == '__main__':
    main()

"""
Simple Core Parameter Definition
4 layers × 36 assemblies = 144 total positions

Demonstrates programmatic MCNP input generation
"""

# Core configuration
# Format: 'NN' = fuel assembly, 'NN_C' = control assembly
assemblies = {
    1: [  # Layer 1 (bottom)
        '01', '02', '03', '04', '05', '06',
        '07', '08_C', '09', '10', '11_C', '12',
        '13', '14', '15', '16', '17', '18',
        '19', '20', '21_C', '22', '23', '24',
        '25', '26', '27', '28', '29_C', '30',
        '31', '32', '33', '34', '35', '36',
    ],

    2: [  # Layer 2
        '01', '02', '03_C', '04', '05', '06',
        '07_C', '08', '09', '10', '11', '12_C',
        '13', '14', '15_C', '16', '17', '18',
        '19', '20_C', '21', '22', '23_C', '24',
        '25', '26_C', '27', '28', '29', '30',
        '31', '32', '33', '34_C', '35', '36',
    ],

    3: [  # Layer 3
        '01', '02', '03', '04_C', '05', '06',
        '07', '08', '09_C', '10', '11', '12',
        '13_C', '14', '15', '16', '17_C', '18',
        '19', '20', '21', '22_C', '23', '24',
        '25_C', '26', '27', '28', '29', '30_C',
        '31', '32', '33', '34', '35', '36',
    ],

    4: [  # Layer 4 (top)
        '01', '02_C', '03', '04', '05', '06',
        '07', '08', '09', '10_C', '11', '12',
        '13', '14', '15', '16_C', '17', '18',
        '19_C', '20', '21', '22', '23', '24',
        '25', '26', '27_C', '28', '29', '30',
        '31', '32_C', '33', '34', '35', '36',
    ],
}

# Assembly-specific parameters
fuel_enrichments = {
    # Central region: higher enrichment
    '15': 5.5, '16': 5.5, '21': 5.5, '22': 5.5,

    # Peripheral: lower enrichment
    '01': 3.5, '06': 3.5, '31': 3.5, '36': 3.5,

    # Default for all others: 4.5%
}

control_positions = {
    # Layer 1
    ('1', '08_C'): 'withdrawn',
    ('1', '11_C'): 'withdrawn',
    ('1', '21_C'): 'inserted',
    ('1', '29_C'): 'withdrawn',

    # Layer 2
    ('2', '03_C'): 'inserted',
    ('2', '07_C'): 'withdrawn',
    ('2', '12_C'): 'withdrawn',
    ('2', '15_C'): 'inserted',
    ('2', '20_C'): 'withdrawn',
    ('2', '23_C'): 'withdrawn',
    ('2', '26_C'): 'inserted',
    ('2', '34_C'): 'withdrawn',

    # Layer 3
    ('3', '04_C'): 'withdrawn',
    ('3', '09_C'): 'inserted',
    ('3', '13_C'): 'withdrawn',
    ('3', '17_C'): 'withdrawn',
    ('3', '22_C'): 'inserted',
    ('3', '25_C'): 'withdrawn',
    ('3', '30_C'): 'withdrawn',

    # Layer 4
    ('4', '02_C'): 'inserted',
    ('4', '10_C'): 'withdrawn',
    ('4', '16_C'): 'withdrawn',
    ('4', '19_C'): 'withdrawn',
    ('4', '27_C'): 'inserted',
    ('4', '32_C'): 'withdrawn',
}

# Geometry parameters (cm)
fuel_radius = 0.41
clad_radius = 0.48
pellet_height = 1.0
active_height = 200.0
assembly_pitch = 21.5

# Material parameters
default_enrichment = 4.5  # %
uo2_density = 10.2  # g/cm³
zr_density = 6.5  # g/cm³
water_temp = 350  # K

# Core parameters
core_radius = 150.0  # cm
reflector_thickness = 30.0  # cm

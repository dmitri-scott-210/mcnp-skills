"""
Microreactor Parameter Definition (HTGR-style)
Demonstrates hierarchical numbering for TRISO fuel

This is a simplified example showing the concept.
For a complete implementation, see the analysis/microreactor_programmatic/ directory.
"""

# Core configuration (simplified - 2 layers, 6 assemblies each)
# In full model: 4 layers × 144 assemblies
assemblies = {
    1: ['01', '02', '03', '04', '05', '06'],  # Layer 1
    2: ['01', '02_C', '03', '04', '05', '06_C'],  # Layer 2 (with control)
}

# Assembly types
# Format: 'NN' = fuel block, 'NN_C' = control block

# TRISO fuel parameters
kernel_radius = 0.0250  # cm (250 μm)
buffer_radius = 0.0350  # cm
ipyc_radius = 0.0390   # cm
sic_radius = 0.0425    # cm
opyc_radius = 0.0465   # cm

# Fuel compact parameters
compact_radius = 0.60   # cm
compact_height = 3.94   # cm
compacts_per_stack = 31

# Fuel channel parameters
channel_radius = 0.70   # cm
channels_per_block = 210  # Hexagonal array

# Assembly parameters
assembly_pitch = 2.77   # cm (hexagonal)
assembly_height = 68.0  # cm
block_radius = 18.0     # cm (equivalent circle for hex)

# Material parameters
uo2_density = 10.4      # g/cm³ (kernel)
buffer_density = 1.1    # g/cm³ (porous carbon)
pyc_density = 1.9       # g/cm³
sic_density = 3.2       # g/cm³
graphite_density = 1.7  # g/cm³

kernel_enrichment = 19.7  # % (TRISO fuel)

# Core parameters
core_radius = 100.0         # cm
reflector_thickness = 80.0  # cm
shield_thickness = 70.0     # cm

# Physics parameters
temperature = 1200  # K (HTGR operating temperature)

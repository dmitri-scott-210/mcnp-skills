# MCNP Physical Constants - Python Tools

This directory contains Python tools for physical constants lookup and unit-aware calculations for MCNP.

## Tools Overview

### 1. constants_lookup.py

Interactive and command-line tool for searching and retrieving fundamental physical constants and particle properties.

**Features:**
- Search for constants by name, symbol, or description
- Display constants in multiple unit systems
- Retrieve particle masses and properties
- Pure Python (no external dependencies)

**Interactive Mode:**
```bash
python constants_lookup.py
```

**Command-Line Examples:**
```bash
# Search for constants
python constants_lookup.py --search "avogadro"
python constants_lookup.py --search "planck"

# Display specific constant
python constants_lookup.py --constant "speed_of_light"
python constants_lookup.py --constant "boltzmann_constant" --unit "eV/K"

# Display particle properties
python constants_lookup.py --particle "neutron"
python constants_lookup.py --particle "electron"

# List all
python constants_lookup.py --list
```

### 2. unit_aware_calculator.py

Scientific calculator with automatic unit handling for common MCNP physics calculations.

**Features:**
- Atom density from mass density
- Thermal energy from temperature
- Neutron speed from energy
- Nuclear Q-values
- Binding energies
- Fission rates
- Decay constants
- Specific activities

**Interactive Mode:**
```bash
python unit_aware_calculator.py
```

**Command-Line Examples:**
```bash
# Atom density calculation
python unit_aware_calculator.py --calc atom_density --density 7.85 --mass 55.845

# Thermal energy calculation
python unit_aware_calculator.py --calc thermal_energy --temperature 600

# Neutron speed calculation
python unit_aware_calculator.py --calc neutron_speed --energy 0.0253 --energy-unit eV
```

## Installation

No installation required. These are standalone Python 3 scripts with no external dependencies.

**Requirements:**
- Python 3.6 or later
- Standard library only

**Make scripts executable (Linux/Mac):**
```bash
chmod +x constants_lookup.py
chmod +x unit_aware_calculator.py
```

## Usage Guide

### constants_lookup.py Detailed Usage

#### Interactive Mode

Launch interactive mode:
```bash
python constants_lookup.py
```

**Available commands in interactive mode:**
- `search <query>` - Search for constants and particles
- `constant <name>` - Display constant information
- `particle <name>` - Display particle information
- `list constants` - List all available constants
- `list particles` - List all available particles
- `help` - Show help
- `quit` or `exit` - Exit program

**Example session:**
```
lookup> search avogadro
SEARCH RESULTS
CONSTANTS (1 matches):
  1. avogadro_constant

lookup> constant avogadro_constant
CONSTANT: avogadro_constant
Symbol:      N_A
Value:       6.0221407600e+23 1/mol
Uncertainty: Exact (by definition)
Description: Avogadro constant (exact by definition since 2019)

lookup> particle neutron
PARTICLE: neutron
Symbol:      n
Mass (kg):   1.6749274980e-27 kg
Mass (amu):  1.008664915950 amu
Mass (MeV):  939.565420520 MeV/c²
Charge:      0 e
Spin:        0.5
Half-life:   8.794000e+02 s
Description: Neutron (unstable when free, t_1/2 = 879.4 s)
```

#### Command-Line Mode

**Search for constants:**
```bash
$ python constants_lookup.py --search "boltzmann"
SEARCH RESULTS
CONSTANTS (1 matches):
  1. boltzmann_constant
```

**Display constant in specific units:**
```bash
$ python constants_lookup.py --constant "boltzmann_constant" --unit "eV/K"
CONSTANT: boltzmann_constant
Symbol:      k_B
Value:       8.6173332620e-05 eV/K
...
```

**Get particle property:**
```bash
$ python constants_lookup.py --particle "electron" --property "mass_MeV"
electron.mass_MeV = 0.51099895000
```

### unit_aware_calculator.py Detailed Usage

#### Interactive Mode

Launch calculator:
```bash
python unit_aware_calculator.py
```

**Available calculations:**
1. Atom density (from mass density)
2. Thermal energy (from temperature)
3. Neutron speed (from energy)
4. Q-value (nuclear reaction)
5. Binding energy
6. Fission rate (from power)
7. Decay constant (from half-life)
8. Specific activity

**Example: Atom Density Calculation**
```
Select calculation (1-8) or command> 1

--- Atom Density Calculation ---
Mass density (g/cm³): 7.85
Atomic mass (g/mol): 55.845

Results:
  Atom density: 8.4603e+22 atoms/cm³
  Atom density: 0.084603 atoms/b-cm

MCNP material card (atom density):
  M#  ZZZAAA.##c  0.084603
```

**Example: Thermal Energy**
```
Select calculation (1-8) or command> 2

--- Thermal Energy Calculation ---
Temperature: 600
Unit (K/C/F) [K]: K

Results:
  Temperature: 600.00 K
  Thermal energy: 5.1704e-02 eV
  Thermal energy: 5.1704e-08 MeV

MCNP TMP card:
  TMP  600.00    $ Temperature in Kelvin
```

**Example: Neutron Speed**
```
Select calculation (1-8) or command> 3

--- Neutron Speed Calculation ---
Energy: 0.0253
Unit (eV/keV/MeV) [MeV]: eV

Results:
  Energy: 0.000000 MeV
  Speed: 2.1998e+03 m/s
  Wavelength: 1.7983e+00 Å
```

#### Command-Line Mode

**Atom density:**
```bash
$ python unit_aware_calculator.py --calc atom_density --density 1.0 --mass 1.008
Atom density: 0.597298 atoms/b-cm
```

**Thermal energy:**
```bash
$ python unit_aware_calculator.py --calc thermal_energy --temperature 293.6
Thermal energy: 2.530065e-08 MeV
```

**Neutron speed:**
```bash
$ python unit_aware_calculator.py --calc neutron_speed --energy 1.0 --energy-unit MeV
Neutron speed: 1.3831e+07 m/s
```

## Physical Constants Database

### Universal Constants (CODATA 2018)

- `speed_of_light` - Speed of light in vacuum (c)
- `planck_constant` - Planck constant (h)
- `reduced_planck_constant` - Reduced Planck constant (ℏ)
- `boltzmann_constant` - Boltzmann constant (k_B)
- `elementary_charge` - Elementary charge (e)
- `avogadro_constant` - Avogadro constant (N_A)

### Electromagnetic Constants

- `permittivity_vacuum` - Permittivity of free space (ε₀)
- `permeability_vacuum` - Permeability of free space (μ₀)
- `fine_structure_constant` - Fine structure constant (α ≈ 1/137)

### Conversion Factors

- `atomic_mass_unit` - Atomic mass unit (amu → kg, MeV/c²)
- `electron_volt` - Electron volt (eV → J)

### Particle Properties

**Leptons:**
- `electron` - Electron properties
- `positron` - Positron properties
- `muon` - Muon properties

**Nucleons:**
- `proton` - Proton properties
- `neutron` - Neutron properties

**Light Nuclei:**
- `deuteron` - Deuterium nucleus (²H)
- `triton` - Tritium nucleus (³H)
- `helium3` - Helium-3 nucleus
- `alpha` - Alpha particle (⁴He)

## Common MCNP Calculations

### 1. Material Definition (Atom Density)

**Problem:** Define iron material at ρ = 7.85 g/cm³

```bash
python unit_aware_calculator.py --calc atom_density --density 7.85 --mass 55.845
```

**Result:** N = 0.0846 atoms/b-cm

**MCNP Card:**
```
M1  26000.80c  0.0846    $ Iron at 7.85 g/cm³
```

### 2. Temperature for Cross Sections

**Problem:** Material at 600 K, express in MeV for TMP card

```bash
python unit_aware_calculator.py --calc thermal_energy --temperature 600
```

**Result:** E = 5.17 × 10⁻⁸ MeV

**MCNP Card:**
```
TMP  600       $ Temperature in Kelvin
c Or:
TMP  5.17E-8   $ Temperature in MeV
```

### 3. Neutron Source Energy

**Problem:** Thermal neutron source at room temperature (20°C = 293.6 K)

```bash
python unit_aware_calculator.py --calc thermal_energy --temperature 293.6
```

**Result:** E_thermal = 0.0253 eV = 2.53 × 10⁻⁸ MeV

**MCNP Card:**
```
SDEF  PAR=1  ERG=2.53E-8    $ Thermal neutron source
```

### 4. Reactor Power from Fission Rate

**Example:** 1 MW reactor

```bash
python unit_aware_calculator.py --calc fission_rate --power 1e6
```

**Result:**
- Fission rate: 3.12 × 10¹⁶ fissions/second
- Fuel consumption: ~1 g U-235/day

## Integration with MCNP Skills

These tools integrate with:

- **mcnp-unit-converter** - Extends with physical constants
- **mcnp-material-builder** - Atom density calculations
- **mcnp-source-builder** - Particle energies and properties
- **mcnp-physics-builder** - Temperature conversions
- **mcnp-isotope-lookup** - Particle masses and decay data

## Extending the Tools

### Adding New Constants

Edit `constants_lookup.py` and add to the `PhysicalConstants.constants` dictionary:

```python
"new_constant": {
    "symbol": "X",
    "value": 1.234e-5,
    "unit": "m/s",
    "uncertainty": 1e-8,
    "alt_values": {
        "cm/s": 1.234e-3,
    },
    "description": "Description of the constant"
}
```

### Adding New Particles

Edit `constants_lookup.py` and add to the `ParticleProperties.particles` dictionary:

```python
"new_particle": {
    "symbol": "X",
    "mass_kg": 1.234e-27,
    "mass_amu": 0.742,
    "mass_MeV": 691.2,
    "charge": 0,
    "spin": 0.5,
    "description": "Description of particle"
}
```

### Adding New Calculations

Edit `unit_aware_calculator.py` and add method to `MCNPCalculator` class:

```python
def new_calculation(self, param1: float, param2: float) -> Dict[str, Any]:
    """
    Description of calculation.

    Args:
        param1: First parameter
        param2: Second parameter

    Returns:
        Dict with results
    """
    result = param1 * param2  # Your calculation

    return {
        "result": result,
        "param1": param1,
        "param2": param2,
    }
```

## References

### Data Sources

**NIST Physical Constants:**
- https://physics.nist.gov/cuu/Constants/
- CODATA 2018 recommended values

**Particle Data Group (PDG):**
- https://pdg.lbl.gov/
- Particle masses and properties (2020)

**IAEA Nuclear Data:**
- https://www-nds.iaea.org/
- Nuclear masses and decay data

### Related Documentation

See the skill reference files in parent directory:
- `fundamental_constants.md` - Complete CODATA 2018 values
- `particle_properties.md` - Detailed particle data
- `nuclear_constants.md` - Nuclear physics constants
- `benchmark_cross_sections.md` - Cross section reference

## Troubleshooting

### Common Issues

**1. "Unknown constant/particle"**
- Use `--list` to see all available names
- Use `--search` to find similar names
- Check spelling (case-insensitive)

**2. "Unknown unit"**
- Check available units with `--constant <name>` (shows alt_values)
- Common units: eV, keV, MeV, J, K, C, F

**3. "Calculation error"**
- Verify input values are reasonable
- Check units match expected input
- Some calculations have physical limits (e.g., non-relativistic approximation)

### Getting Help

For detailed help on any tool:
```bash
python constants_lookup.py --help
python unit_aware_calculator.py --help
```

In interactive mode, type `help` at the prompt.

## License

These tools are part of the MCNP Skills Project. Use freely for MCNP work and nuclear engineering calculations.

## Version History

**v2.0.0 (2025-11-06):**
- Complete rewrite with CODATA 2018 values
- Added unit-aware calculator
- Standalone tools (no external dependencies)
- Interactive and command-line modes

---

**For more information, see the parent SKILL.md file.**

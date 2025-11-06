# MCNP Template Generator - Python Tool

## Usage

**Interactive Mode**:
```bash
python template_generator.py
```

**Command-Line Mode**:
```bash
python template_generator.py --type shielding
python template_generator.py --type criticality --output my_crit.i
python template_generator.py --type dose
```

## Available Templates

1. **Shielding** - Spherical shield around point source
2. **Criticality** - Bare fissile sphere (KCODE)
3. **Dose** - Ambient dose equivalent calculation

## Customization

Templates use `[PARAMETER]` placeholders. Replace with actual values:

```bash
sed -i 's/\[SHIELD_RADIUS_CM\]/10.0/g' shielding_sphere.i
sed -i 's/\[SOURCE_STRENGTH\]/1.0E10/g' shielding_sphere.i
```

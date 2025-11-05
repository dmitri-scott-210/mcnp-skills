# MCNP Geometry Checker - Scripts

**Version:** 2.0.0

## Overview
Python scripts for automated geometry validation.

## Usage

```bash
python mcnp_geometry_checker.py input.inp
```

**Output:**
- Errors: Geometry problems (must fix)
- Warnings: Potential issues
- Recommendations: Best practices

## Integration

```python
from mcnp_geometry_checker import MCNPGeometryChecker

checker = MCNPGeometryChecker()
issues = checker.check_geometry('input.inp')
```

---

**See SKILL.md for complete usage examples**

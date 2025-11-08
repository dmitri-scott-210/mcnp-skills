# scripts/ Directory

**Purpose:** Executable Python/Bash scripts for automation

## What Goes Here

- **Python automation modules** - Tools mentioned in SKILL.md
- **Validation scripts** - Input checking, error detection
- **Helper utilities** - Repeated operations, conversions
- **requirements.txt** - Python dependencies

## When to Use scripts/

✅ **DO bundle scripts when:**
- SKILL.md mentions Python automation
- Operation is repeatedly rewritten
- Reliability is critical (validation, checking)
- Complex algorithm better as executable code

❌ **DON'T bundle scripts for:**
- One-off code snippets
- Simple demonstrations
- User-customized code

## File Naming

- `mcnp_[function].py` - Main automation tools
- `validate_[aspect].py` - Validation tools
- `helper_[task].py` - Utility functions
- `requirements.txt` - Dependencies

## Documentation Requirements

Each script needs:
1. **Docstring** at top explaining purpose
2. **Function/class documentation**
3. **Usage examples** in comments or this README
4. **Error handling** documented
5. **Dependencies** listed in requirements.txt

## README Contents

Include in this README:
- **Script inventory** - List all scripts with purpose
- **API documentation** - Function signatures, parameters, returns
- **Usage examples** - How to invoke each script
- **Installation** - How to install dependencies
- **Error handling** - Common errors and solutions

## Example

```python
# mcnp_input_validator.py
"""
MCNP Input File Validator

Validates MCNP input files for syntax errors, cross-references,
and formatting issues before expensive simulation runs.

Usage:
    python mcnp_input_validator.py input.i

Returns:
    0 if valid, 1 if errors found
"""

def validate_input_file(filepath):
    """
    Validate MCNP input file

    Args:
        filepath (str): Path to MCNP input file

    Returns:
        dict: {
            'valid': bool,
            'errors': list,
            'warnings': list
        }
    """
    pass
```

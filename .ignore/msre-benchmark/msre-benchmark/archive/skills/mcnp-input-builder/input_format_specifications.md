# MCNP Input Format Specifications

**Reference Document for mcnp-input-builder Skill**

This document provides detailed specifications for MCNP6 input file formatting, including card continuation rules, comment syntax, input shortcuts, numerical limitations, and default units.

---

## Input Line Format

### Character Limit
- **Maximum:** 128 characters per line
- **Note:** Older documentation references 80 columns, but MCNP6 supports up to 128
- **Recommendation:** Keep lines ≤80 characters for readability and compatibility

### Column Conventions
- **Columns 1-5:** Card name or blank for continuation
- **Column 6 onward:** Card parameters and data
- **Tabs:** Treated as single spaces (NOT multiple spaces)
  - **Critical:** Always use spaces, never tabs
  - Configure text editor to convert tabs to spaces

---

## Card Continuation Methods

MCNP provides several methods for continuing cards across multiple lines:

### Method 1: Five-Space Continuation (Recommended)
Leave columns 1-5 blank (5 or more leading spaces):

```
F4:N  1 2 3 4 5 6 7 8 9 10
      11 12 13 14 15 16 17
      18 19 20
```

**Advantages:**
- Clean appearance
- Clear visual continuation
- No special characters needed

### Method 2: Ampersand Continuation
End line with `&` character:

```
F4:N  1 2 3 4 5 6 7 8 9 10 &
      11 12 13 14 15 16 17 &
      18 19 20
```

**Advantages:**
- Explicit continuation marker
- Useful for clarity in complex cards

### Method 3: Card Name Repetition
Repeat the card name on each line:

```
F4:N  1 2 3 4 5
F4:N  6 7 8 9 10
F4:N  11 12 13 14 15
```

**Advantages:**
- Each line is self-documenting
- Useful for programmatically generated inputs

### Method 4: Vertical Format (Advanced)
Use `#` in columns 1-5 to activate vertical format:

```
#     F4:N  E4    T4
      1     0.1   0
      2     1.0   1E-8
      3     10    1E-7
      4     100   1E-6
```

**Format:**
- First line after `#`: Card names in columns
- Subsequent lines: Data values in corresponding columns
- **Use case:** Tabular data with multiple related cards

---

## Comment Syntax

### Full-Line Comments
Comment lines start with `c` (lowercase or uppercase) in columns 1-5, followed by space:

```
C This is a comment line
c This is also a comment (lowercase works)
```

**Rules:**
- Character 'C' or 'c' must be in columns 1-5
- Must be followed by a space (column 6)
- Entire line treated as comment

**Common usage:**
```
c =================================================================
c SECTION HEADER
c =================================================================
c  Description of the following cards
c  - Detail 1
c  - Detail 2
c -----------------------------------------------------------------
```

### Inline Comments
Use `$` to comment remainder of line:

```
F4:N  1                                       $ Flux in cell 1
M1   1001  2  8016  1                        $ Water H2O
MODE  N                                       $ Neutron transport only
```

**Rules:**
- `$` can appear anywhere on line (not just columns 1-5)
- Everything after `$` is ignored
- Useful for documenting parameters

### Comment Best Practices
1. Use full-line comments for section headers
2. Use inline comments for parameter explanations
3. Create visual separators with `=` or `-` characters
4. Document non-obvious choices (e.g., why specific density used)
5. Include units when ambiguous

---

## Card Naming Conventions

### Cell Cards
- **Range:** 1 to 99,999,999
- **No gaps required:** Can use 1, 5, 10, 100, etc.
- **Namespace:** Independent from surface cards (same numbers allowed)

**Recommended grouping:**
```
1-99      = Core region
100-199   = Reflector region
200-299   = Shield region
300-399   = Detector region
900-999   = Graveyard cells
```

### Surface Cards
- **Range:** 1 to 99,999,999
- **No gaps required**
- **Namespace:** Independent from cell cards

**Recommended grouping:**
```
1-9       = Inner boundaries
10-19     = Outer boundaries
20-29     = Auxiliary surfaces
100-199   = Complex geometry surfaces
```

### Data Cards
- **Format:** Alphabetic mnemonics with optional numbers
- **Particle designators:** Colon + particle symbol (`:N`, `:P`, `:E`)
- **Numbered variants:**
  - Tallies: F4, F14, F24, F34, ... (4, 14, 24, ...)
  - Materials: M1, M2, M3, ... (1, 2, 3, ...)
  - Transformations: TR1, TR2, TR3, ... (1-999)
  - Energy bins: E4, E14, E24, ... (matches tally number)

---

## Input Shortcuts

MCNP provides shortcuts for repetitive data entry:

### R - Repeat
Repeat the previous entry `n` times:

```
E4  0.01 0.1 1 10 100         $ Standard entry
E4  0.01 3R 100                $ Same as: 0.01 0.01 0.01 0.01 100
```

**Format:** `nR` where n = number of repetitions
**Note:** Repeats the immediately preceding value

### I - Interpolate
Insert `n` linearly interpolated values:

```
E4  0.01 2I 1.0                $ Generates: 0.01 0.34 0.67 1.0
E4  1 4I 10                    $ Generates: 1 2.8 4.6 6.4 8.2 10
```

**Format:** `nI` where n = number of interpolated points
**Calculation:** Linear spacing between previous and next value

### M - Multiply
Multiply all subsequent entries by factor:

```
IMP:N  1 8M                    $ Same as: 1 8 64 512 4096 ...
IMP:N  1 2M                    $ Same as: 1 2 4 8 16 32 ...
```

**Format:** `nM` where n = multiplication factor
**Note:** Applies to all entries that follow on the card

### J - Jump (Default)
Use default value for `n` positions:

```
PHYS:N  100 J J 1              $ Use defaults for 2nd and 3rd parameters
PHYS:N  100 2J 1               $ Same as above
```

**Format:** `nJ` where n = number of positions to skip
**Note:** Uses MCNP default values for skipped parameters

### LOG - Logarithmic Interpolate
Insert `n` logarithmically spaced values:

```
E4  0.01 3LOG 10               $ Logarithmic spacing from 0.01 to 10
E4  1E-6 5LOG 1                $ Logarithmic spacing from 1E-6 to 1
```

**Format:** `nLOG` where n = number of points
**Use case:** Energy bins over multiple decades

### ILOG - Integer Logarithmic
Similar to LOG but rounds to integers:

```
NPS  1000 2ILOG 1000000        $ Generates: 1000, 31623, 1000000
```

**Format:** `nILOG`
**Use case:** NPS progression for convergence studies

---

## Numerical Limitations

MCNP6 has built-in limits on various identifiers:

| Item | Range | Notes |
|------|-------|-------|
| Cell numbers | 1 - 99,999,999 | No gaps required |
| Surface numbers | 1 - 99,999,999 | No gaps required |
| Material numbers | 1 - 99,999,999 | No gaps required |
| Transformation numbers | 1 - 999 | TRn cards |
| Tally numbers | 1, 2, ..., 9, 11, 12, ..., 99,999,999 | Special restrictions for some types |
| Universe numbers | 0 - 99,999,999 | 0 = main universe |
| Distribution numbers | 1 - 999 | For SI, SP, SB cards |

**Important:**
- No gaps required in numbering (can use sparse numbers)
- Cell, surface, and material numbers are in separate namespaces
- Avoid excessively large numbers (complicates debugging)

---

## Message Block Format

The optional message block appears before the title card:

### Standard Format
```
MESSAGE:
This is an optional message block that can contain
multiple lines of descriptive text about the problem.
It ends with a blank line.

Title Card Starts Here
c =================================================================
c Cell Cards
c =================================================================
...
```

### Format Rules
- **Starts with:** `MESSAGE:` keyword (capital letters)
- **Contains:** Arbitrary text (multiple lines allowed)
- **Ends with:** Blank line
- **Purpose:** Documentation, problem description, metadata

### Alternative: Simple Title
If no `MESSAGE:` block is used, the first line is the title card:

```
Simple Problem Title - Water Sphere
c =================================================================
c Cell Cards
c =================================================================
...
```

---

## Default Units

MCNP uses consistent units across all input cards:

| Quantity | Unit | Notes |
|----------|------|-------|
| **Length** | centimeters (cm) | All geometric dimensions |
| **Energy** | MeV | Particle energies, energy bins |
| **Time** | shakes | 1 shake = 10⁻⁸ seconds |
| **Temperature** | MeV | k·T where k = Boltzmann constant (8.617×10⁻¹¹ MeV/K) |
| **Mass Density** | g/cm³ | Positive values in cell cards |
| **Atomic Density** | atoms/(barn·cm) | Negative values in cell cards (1 barn = 10⁻²⁴ cm²) |
| **Cross Sections** | barns | 1 barn = 10⁻²⁴ cm² |
| **Angle** | degrees or cosines | Depends on card (SDEF uses degrees, DIR uses cosines) |

### Temperature Conversion
To convert from Kelvin to MeV for TMP card:

```
T_MeV = k * T_K = 8.617×10⁻¹¹ * T_K

Examples:
- 293 K (room temp) = 2.53×10⁻⁸ MeV
- 600 K            = 5.17×10⁻⁸ MeV
- 900 K            = 7.76×10⁻⁸ MeV
```

### Density Specification
**Positive value:** Mass density in g/cm³
```
1    1  8.0    -1    IMP:N=1        $ 8.0 g/cm³ (steel)
```

**Negative value:** Atomic density in atoms/(barn·cm)
```
1    1  -0.1   -1    IMP:N=1        $ 0.1 atoms/(barn·cm)
```

**Conversion:**
```
ρ_atomic = (ρ_mass * N_A) / (A * 1×10²⁴)

Where:
- ρ_mass = mass density (g/cm³)
- N_A = Avogadro's number (6.022×10²³ /mol)
- A = atomic/molecular weight (g/mol)
- Factor 1×10²⁴ converts cm² to barns
```

---

## Input File Termination

Every MCNP input file must end with a blank line:

```
...
NPS  1000000
PRINT
<--- BLANK LINE REQUIRED HERE (end of file)
```

**Why important:**
- MCNP reads until blank line
- Without it, input may not terminate properly
- Can cause "bad trouble" errors

---

## Character Encoding

### Supported Characters
- **Alphanumeric:** A-Z, a-z, 0-9
- **Special:** Space, ., -, +, =, :, $, &, #, /, *, (, )
- **Comments:** Any ASCII characters in comments

### Unsupported Characters
- **Tabs:** Converted to single space (use spaces instead)
- **Non-ASCII:** May cause issues (avoid international characters)

---

## Common Formatting Errors

### Error 1: Tabs Instead of Spaces
**Problem:** MCNP treats tabs as single spaces, breaking alignment

**Bad:**
```
F4:N	1	2	3        (tabs between entries)
```

**Good:**
```
F4:N  1  2  3        (spaces between entries)
```

### Error 2: Missing Blank Lines
**Problem:** Blocks not properly terminated

**Bad:**
```
1  1  -1.0  -1  IMP:N=1
2  0        1   IMP:N=0
1  SO  10.0              $ Missing blank line between blocks
MODE N
```

**Good:**
```
1  1  -1.0  -1  IMP:N=1
2  0        1   IMP:N=0
                         $ Blank line separates blocks
1  SO  10.0
                         $ Another blank line
MODE N
```

### Error 3: Comment in Columns 1-5 Without Space
**Problem:** 'C' must be in columns 1-5 AND followed by space

**Bad:**
```
CThis is a comment       $ No space after C
```

**Good:**
```
C This is a comment      $ Space in column 6
```

---

## Quick Reference: Formatting Rules

1. **Line length:** ≤128 characters (recommend ≤80)
2. **Card continuation:** 5+ leading spaces, `&`, or card name repeat
3. **Comments:** `C` in columns 1-5 + space (full line) or `$` (inline)
4. **Blank lines:** Required between blocks and at end of file
5. **Tabs:** Never use tabs (always use spaces)
6. **Case:** MCNP is case-insensitive (except for filenames on some systems)
7. **Units:** cm, MeV, shakes, g/cm³ (positive) or atoms/(barn·cm) (negative)

---

## Further Reading

- MCNP6 User Manual, Chapter 4: Description of MCNP6 Input
- MCNP6 User Manual, Chapter 3: Introduction to MCNP Usage
- Skill: mcnp-input-validator (for automated format checking)

---

**End of Input Format Specifications**

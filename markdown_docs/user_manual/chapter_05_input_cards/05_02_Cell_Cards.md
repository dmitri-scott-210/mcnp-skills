---
title: "Chapter 5.2 - Cell Cards"
chapter: "5.2"
source_pdf: "mcnp631_theory_user-manual/mcnp-user-manual-chapters/5_Input_Cards/5.2_Cell_Cards.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

description of cell n . In other words, a number immediately after a
complement operator, without parentheses, is interpreted as a cell
number and is shorthand for the geometry specification of that cell
number. The notation #( ... ) , where ( ... ) is usually a list of
surfaces describing another cell, means to complement the portion of the
cell description in parentheses. Note that the symbol '#' is also used
to denote heavy ions; however, the meaning of the symbol in the input
file is obvious from how and where it is applied.

The default order of operations is complement first, intersection
second, and unions third. There is no right-to-left ordering.
Parentheses can be used to clarify operations and in some cases are
required to force a certain order of operations. Innermost parentheses
are cleared first. Spaces are optional on either side of a parenthesis.
A parenthesis is equivalent to a space and signifies an intersection.
Parentheses and operator symbols also function as delimiters; where they
are present, blank delimiters are not necessary.

## 5.2 Cell Cards

Recommended precautions when creating cell definitions include the
following:

1. Avoid excessively complicated cells. A problem geometry constructed of numerous simple cells runs faster than the same problem described using fewer, more complicated cells.
2. Avoid ineffective use of the complement operator, which can cause unneeded surfaces to be added to the geometry description of a cell. Extra surfaces make the problem run more slowly and may destroy the necessary conditions for volume and area calculations. See the example in §10.1.1.14.
3. Always use the geometry-plotting feature of MCNP6 to check the geometry of a problem [§6.2].
4. Flood the system with particles from an outside source to find errors in the geometry [§4.8].
5. If you add or remove cells, remember to change all the cell parameter cards accordingly. The difficulty of this can be reduced if the vertical format is used to specify values on the cell parameter cards [§4.4.5.2]. Alternatively, define cell-parameter values directly on cell cards and eliminate cell parameter cards entirely.

```
Form 1: j m d geom params Form 2: j LIKE n BUT list ( 1 ) j Cell number assigned by the user. Restriction: 1 ≤ j ≤ 99 , 999 , 999 Restriction: If the cell is affected by a TRCL transformation, then j must be in the range 1 ≤ j ≤ 999 . m Material number if the cell is not a void. Restriction: 1 ≤ m ≤ 99 , 999 , 999 m > 0 the cell contains material m, which is specified on the M m card located in the data card section of the MCNP input file. m = 0 the cell is a void. d Cell material density. This parameter is absent if the cell is a void. d > 0 interpret the value as the atomic density in units of 10 24 atoms/cm 3 (i.e., atoms/b-cm).
```

|        | d < 0                                                                                                                                                                                                                                                                                                                            | interpret the value as the mass density in units of g/cm 3 .                                                                                                                                                                                                                                                                     |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| geom   | Specification of the geometry of the cell. This specification consists of signed surface numbers and Boolean operators that specify how the regions bounded by the surfaces are to be combined. Boolean operators include the following:                                                                                         | Specification of the geometry of the cell. This specification consists of signed surface numbers and Boolean operators that specify how the regions bounded by the surfaces are to be combined. Boolean operators include the following:                                                                                         |
|        | <space>                                                                                                                                                                                                                                                                                                                          | indicates intersection,                                                                                                                                                                                                                                                                                                          |
|        | :                                                                                                                                                                                                                                                                                                                                | indicates union; and                                                                                                                                                                                                                                                                                                             |
|        | #                                                                                                                                                                                                                                                                                                                                | indicates complement.                                                                                                                                                                                                                                                                                                            |
| params | Optional specification of cell parameters by entries in the KEYWORD = value form. Allowed keywords include IMP , VOL , PWT , EXT , FCL , WWN , DXC , NONU , PD , TMP , U , TRCL , LAT , FILL , ELPT , COSY , BFLCL , and UNC ( 2 , 3 ).                                                                                          | Optional specification of cell parameters by entries in the KEYWORD = value form. Allowed keywords include IMP , VOL , PWT , EXT , FCL , WWN , DXC , NONU , PD , TMP , U , TRCL , LAT , FILL , ELPT , COSY , BFLCL , and UNC ( 2 , 3 ).                                                                                          |
| n      | Number of another cell. Restriction: Cell card for cell n must appear in the MCNP input file before                                                                                                                                                                                                                              | Number of another cell. Restriction: Cell card for cell n must appear in the MCNP input file before                                                                                                                                                                                                                              |
| list   | Set of KEYWORD = value specifications that define the attributes that differ between cells n and j . Allowed keywords include MAT (material number) and RHO (density) as well as the cell parameter keywords IMP , VOL , PWT , EXT , FCL , WWN , DXC , NONU , PD , TMP , U , TRCL , LAT , FILL , ELPT , COSY , BFLCL , and UNC . | Set of KEYWORD = value specifications that define the attributes that differ between cells n and j . Allowed keywords include MAT (material number) and RHO (density) as well as the cell parameter keywords IMP , VOL , PWT , EXT , FCL , WWN , DXC , NONU , PD , TMP , U , TRCL , LAT , FILL , ELPT , COSY , BFLCL , and UNC . |

## Details:

- 1 The LIKE n BUT feature is very useful in problems with many repeated structures. Cell j inherits from cell n the values of all attributes that are not specified in the list. The cell card for cell n must be before the cell card for cell j in the MCNP input file. The LIKE n BUT feature uses keywords for the cell material number and density. The mnemonics are MAT and RHO , respectively. These two keywords are only allowed following the LIKE n BUT construct, and may not appear in a normal cell description. Any other keyword name that appears after the BUT is a cell parameter and, therefore, must appear on cell cards only, not on any cards in the data block of the MCNP input file.
- 2 Cell parameters may be defined on cell cards instead of in the data card section of the MCNP input file. If a cell parameter is entered on any cell card, a cell-parameter card with that name cannot be present, nor can the mnemonic appear on any vertical-format input card. It is permitted for some cell parameters to be specified on cell cards, while other subsets are specified in the data section. The format for cell parameters defined on cell cards is KEYWORD = value(s) , where the allowed keywords are IMP , VOL , PWT , EXT , FCL , WWN , DXC , NONU , PD , TMP , U , TRCL , LAT , FILL , ELPT , COSY , BFLCL , and UNC , with particle designators where necessary. The cell-parameter cards associated with the repeated structures capability, U , LAT , and FILL , may be placed either on the cell cards or in the data card section of the MCNP input file (see the U , LAT , and FILL cards).
- 3 TMP and WWN data can be entered on cell cards in two ways. The KEYWORD = value form ( TMP1= value TMP2= value ... ) can be used or a special syntax is available where the single keyword TMP is followed by all the temperatures of the cell in an order corresponding to the times on the THTME card. The form for the WWN keyword is analogous: WWN1: n = value or WWN: n followed by all the lower weight bounds for the energy intervals of the cell.

## Example 1
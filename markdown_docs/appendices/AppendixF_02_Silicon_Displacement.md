---
title: "Appendix F.2 - Silicon Displacement Factors"
chapter: "F.2"
source_pdf: "mcnp631_theory_user-manual/appendecies/F.2_Silicon_Displacement_Factors.pdf"
conversion_date: "2025-10-30"
converted_by: "Docling MCP Server + Claude"
notes: "Converted from MCNP6.3.1 documentation"
---

## F.2 Silicon Displacement Factors

Radiation damage to or effects on electronic components are often of
interest. Of particular interest are the absorbed dose in rads and
silicon displacement kerma factors. The absorbed dose may be calculated
for a specific material by using the FM tally card with an appropriate
multiplicative constant c to convert from the default MCNP units to
rads. The silicon displacement kermas, however, are given as a function
of energy, similar to the biological conversion factors. Therefore, they
may be implemented on the DE and DF cards. One source of these kerma
factors and a discussion of their significance is available in [365]
with additional details in [366].
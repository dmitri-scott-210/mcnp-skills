cat << 'EOF2' > /home/user/mcnp-skills/.claude/skills/mcnp-template-generator/template_customization_guide.md &&
wc -l /home/user/mcnp-skills/.claude/skills/mcnp-template-generator/templates/*.i /home/user/mcnp-skills/.claude/skills/mcnp-template-generator/*.md
c ===================================================================
c TEMPLATE: Bare Criticality Sphere
c ===================================================================
c DESCRIPTION: Bare fissile sphere for keff calculation
c PARAMETERS TO CUSTOMIZE:
c   Core radius: 8.0 cm
c   U-235 density: 18.75 g/cm³ (metal density)
c ===================================================================

c Cell Cards
1  1  -18.75  -1  IMP:N=1  $ Fissile core (U-235 metal)
2  0   1  IMP:N=0  $ Void outside

c Surface Cards
1  SO  8.0  $ Core outer surface (8 cm radius)

c Data Cards
MODE  N
KCODE  10000  1.0  50  250  $ 10K/cycle, guess=1.0, skip 50, run 250
KSRC  0 0 0  $ Initial source at center
M1  92235.80c  1.0  $ U-235 metal (100%)
F4:N  1  $ Average flux in core
F7:N  1  $ Fission rate in core

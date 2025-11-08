# references/ Directory

**Purpose:** Detailed documentation loaded into Claude's context as needed

## What Goes Here

- **Detailed specifications** (>500 words on single topic)
- **Card format references** (complete syntax for all cards)
- **Theory and background** (mathematical derivations, physics)
- **Comprehensive error catalogs** (all error patterns with fixes)
- **Large example collections** (10-15+ detailed examples)

## Organization

Create topic-specific files:
- `card_specifications.md` - All card formats and syntax
- `theory_background.md` - Mathematical/physical foundations
- `detailed_examples.md` - Comprehensive example collection
- `error_catalog.md` - All errors and troubleshooting
- `[topic].md` - Additional topic-specific files as needed

## Best Practices

1. **No duplication with SKILL.md** - Keep workflow in SKILL.md, details here
2. **Include grep patterns** - For files >2,000 lines, add search patterns
3. **Cross-reference in SKILL.md** - Point to specific files/sections
4. **Progressive detail** - Start with overview, then deep-dive sections

## Example Structure

```markdown
# Card Specifications Reference

## Contents
- Cell Cards (§1)
- Surface Cards (§2)
- Data Cards (§3)

## §1: Cell Cards

### Format
j m d geom params

### Parameters
...
[Detailed specifications]

## Grep Patterns
grep -i "cell card" references/card_specifications.md
grep -A 5 "surface type" references/card_specifications.md
```

## Token Efficiency

- References loaded ONLY when referenced
- Keep SKILL.md lean (<3k words)
- References can be unlimited size
- Users can search/grep large files

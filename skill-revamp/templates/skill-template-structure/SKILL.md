---
name: skill-name
description: "Third-person description of when to use this skill. Be specific about trigger conditions and scenarios."
version: "2.0.0"
dependencies: "python>=3.8, package-name" # Optional - only if external tools needed
---

# [Skill Name]

## Overview

[2-3 paragraphs explaining what this skill does, why it's useful, and when to use it]

Paragraph 1: What this skill does
Paragraph 2: Why/when users need this skill
Paragraph 3: High-level approach

## When to Use This Skill

- [Specific trigger condition 1]
- [Specific trigger condition 2]
- [Specific trigger condition 3]
- [Specific trigger condition 4]
- [Specific trigger condition 5]
- [Additional conditions as needed - aim for 5-10 total]

## Decision Tree

```
[ASCII art decision tree showing workflow]

Example:
Start
  ↓
Question about user need?
  ├─→ Option A → Use this skill
  └─→ Option B → Use other-skill
       ↓
  Follow-up question?
       ├─→ Yes → Also use complementary-skill
       └─→ No → Continue
            ↓
       Validate?
            └─→ Yes → Use validation-skill
```

## Quick Reference

| Concept | Description | Example |
|---------|-------------|---------|
| Key Concept 1 | Brief explanation | `example syntax` |
| Key Concept 2 | Brief explanation | `example syntax` |
| Key Concept 3 | Brief explanation | `example syntax` |

[Add rows as needed - create 1-page cheat sheet]

## Use Cases

### Use Case 1: [Descriptive Title]

**Scenario:** [Problem description - what situation is the user facing?]

**Goal:** [What the user wants to achieve]

**Approach:** [Strategy/method to solve the problem]

**Implementation:**
```
[Code or MCNP input demonstrating the solution]
[Include inline comments explaining key parts]
```

**Key Points:**
- [Important detail about why this works]
- [Common pitfall to avoid]
- [Consideration for this approach]
- [When to use variations]

**Expected Results:** [What output/results should look like]

### Use Case 2: [Another Title]

[Repeat format above - aim for 3-5 use cases total, ranging from simple to complex]

### Use Case 3: [Advanced Example]

[Continue pattern...]

## Integration with Other Skills

**Typical Workflow:**
1. [skill-before] → Do prerequisite task
2. **[THIS SKILL]** → Core task
3. [skill-after] → Follow-up task

**Complementary Skills:**
- [related-skill-1]: Use when [specific condition]
- [related-skill-2]: Provides [complementary functionality]

**Example Complete Workflow:**
```
Project Goal: [Overall objective]

Step 1: [skill-a] - [purpose]
Step 2: [THIS SKILL] - [purpose]
Step 3: [skill-b] - [purpose]
Step 4: [skill-c] - [purpose]
Result: [Final output]
```

## References

**Detailed Information:**
- [Topic 1]: See `references/[filename].md`
- [Topic 2]: See `references/[filename].md`
- [Topic 3]: See `references/[filename].md`

**Templates and Examples:**
- Input templates: See `assets/templates/`
- Validated examples: See `assets/example_inputs/`

**Automation Tools:**
- Python scripts: See `scripts/README.md`
- [Script description]: `scripts/[script-name].py`

**External Documentation:**
- [Reference 1]: [Source and location]
- [Reference 2]: [Source and location]

## Best Practices

1. [First best practice - most important]
2. [Second best practice]
3. [Third best practice]
4. [Fourth best practice]
5. [Fifth best practice]
6. [Sixth best practice]
7. [Seventh best practice]
8. [Eighth best practice]
9. [Ninth best practice]
10. [Tenth best practice]

[Each should be actionable and based on common issues/pitfalls]

---

**Target Word Count:** <3,000 words (preferred), <5,000 words (maximum)
**Target Line Count:** ~600-800 lines

**Remember:**
- Extract large content (>500 words) to references/
- Include 5-10 examples from example_files/ in assets/
- Bundle mentioned scripts in scripts/
- No duplication between SKILL.md and references/
- Use imperative/infinitive voice, not second person

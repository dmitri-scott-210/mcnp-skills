# Skill Revamp Quality Checklist (25 Items)

**Use this checklist for EVERY skill before marking complete**

**Skill Name:** _______________________
**Date:** _______________________
**Reviewer:** Claude Session _______

---

## YAML Frontmatter (5 items)

- [ ] **1. name: field present and matches skill directory name exactly**
  - Current: ________________
  - Expected: ________________
  - ✅ Match / ❌ Fix needed

- [ ] **2. description: field is third-person and trigger-specific**
  - Current: ________________
  - ✅ Good / ❌ Needs revision
  - Trigger conditions clearly stated?
  - Specific about when to use?

- [ ] **3. No non-standard fields (removed activation_keywords, category)**
  - activation_keywords present? ❌ Remove
  - category present? ❌ Remove
  - Other non-standard fields? List: ________________

- [ ] **4. version: field present (use "2.0.0" for revamped skills)**
  - Current: ________________
  - ✅ Present / ❌ Add "2.0.0"

- [ ] **5. dependencies: field present if skill uses external tools**
  - Uses Python modules? List: ________________
  - Uses external tools? List: ________________
  - ✅ Added / ❌ Add / N/A

---

## SKILL.md Structure (10 items)

- [ ] **6. Overview section present (2-3 paragraphs)**
  - Explains what, why, when?
  - ✅ Present / ❌ Add

- [ ] **7. "When to Use This Skill" section with bulleted conditions**
  - Has bulleted list?
  - 5-10 trigger conditions?
  - Specific and actionable?
  - ✅ Good / ❌ Improve

- [ ] **8. Decision tree diagram present (ASCII art)**
  - Shows workflow?
  - Includes decision points?
  - References other skills?
  - ✅ Present / ❌ Add

- [ ] **9. Quick reference table present**
  - Summary format?
  - Key concepts captured?
  - 1-page cheat sheet style?
  - ✅ Present / ❌ Add

- [ ] **10. 3-5 use cases with standardized format**
  - Each has: Scenario, Goal, Implementation, Key Points, Expected Results?
  - Range from simple to complex?
  - Count: _____ (need 3-5)
  - ✅ Sufficient / ❌ Add more

- [ ] **11. Integration section documents connections to other skills**
  - Lists skills to use before?
  - Lists skills to use after?
  - Shows workflow chains?
  - ✅ Complete / ❌ Expand

- [ ] **12. References section points to bundled resources**
  - Points to references/ files?
  - Points to assets/ files?
  - Points to scripts/ files?
  - ✅ Complete / ❌ Add links

- [ ] **13. Best practices section with 10 numbered items**
  - Has exactly 10 items?
  - Actionable recommendations?
  - Based on common pitfalls?
  - Count: _____ (need 10)
  - ✅ Complete / ❌ Add items

- [ ] **14. Word count <3k (preferred) or <5k (maximum)**
  - Current word count: _____ words
  - Current line count: _____ lines
  - ✅ Under 3k / ⚠️ 3-5k (acceptable) / ❌ Over 5k (must reduce)

- [ ] **15. No duplication with references/ content**
  - Checked for repeated specifications?
  - Checked for repeated examples?
  - SKILL.md is workflow guide, references/ are details?
  - ✅ No duplication / ❌ Remove duplicates

---

## Bundled Resources (7 items)

- [ ] **16. references/ directory exists with relevant content**
  - Directory created? ✅ / ❌
  - Contains files: List ________________
  - Appropriate content extracted?
  - ✅ Complete / ❌ Create/populate

- [ ] **17. Large content (>500 words single topic) extracted to references/**
  - Card specifications extracted?
  - Theory sections extracted?
  - Large examples extracted?
  - Error catalogs extracted?
  - ✅ Extracted / ❌ Extract more

- [ ] **18. scripts/ directory exists if skill mentions automation**
  - Skill mentions Python modules? ✅ / ❌ / N/A
  - scripts/ directory created? ✅ / ❌ / N/A
  - Contains files: List ________________
  - ✅ Complete / ❌ Create/bundle / N/A

- [ ] **19. Python modules in scripts/ are functional**
  - Modules execute without errors?
  - README.md explains usage?
  - Dependencies listed?
  - ✅ Functional / ❌ Fix / N/A

- [ ] **20. assets/ directory has relevant examples from example_files/**
  - assets/ directory created? ✅ / ❌
  - Contains 5-10 example files? Count: _____
  - Examples from appropriate category?
  - Basic → Advanced range?
  - ✅ Complete / ❌ Add more examples

- [ ] **21. assets/templates/ has template files (if applicable)**
  - Template files created? ✅ / ❌ / N/A
  - Templates cover basic/intermediate/advanced? ✅ / ❌ / N/A
  - ✅ Complete / ❌ Add templates / N/A

- [ ] **22. Each example has description/explanation**
  - Every .i file has matching _description.txt?
  - Descriptions include: purpose, key features, expected results?
  - Complexity level noted?
  - Related skills listed?
  - ✅ All described / ❌ Add descriptions

---

## Content Quality (3 items)

- [ ] **23. All code examples are valid MCNP syntax**
  - Checked cell card syntax?
  - Checked surface card syntax?
  - Checked data card syntax?
  - No obvious errors?
  - ✅ Valid / ❌ Fix syntax errors

- [ ] **24. Cross-references to other skills are accurate**
  - All mentioned skills exist?
  - Skill names spelled correctly?
  - Workflow chains make sense?
  - ✅ Accurate / ❌ Fix references

- [ ] **25. Documentation references are correct (file paths, sections)**
  - references/ paths correct?
  - assets/ paths correct?
  - scripts/ paths correct?
  - Chapter/section numbers correct?
  - ✅ Correct / ❌ Fix paths

---

## FINAL VALIDATION

**All 25 items checked?** ✅ / ❌

**If ANY item fails:**
- Document the issue
- Fix before proceeding
- Re-run checklist

**If ALL items pass:**
- ✅ Skill revamp COMPLETE
- Update REVAMP-PROJECT-STATUS.md
- Move to next skill

---

## Notes / Issues Found

[Space for notes during checklist review]

________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________

---

**Signed off by:** Claude Session _____ on Date _______
**Status:** ✅ APPROVED / ❌ NEEDS REVISION

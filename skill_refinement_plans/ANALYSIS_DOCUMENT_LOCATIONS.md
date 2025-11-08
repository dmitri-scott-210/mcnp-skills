# Analysis Document Locations Reference

**Purpose**: Quick reference for correct file paths to all analysis documents
**Created**: November 7, 2025

---

## 📁 DIRECTORY STRUCTURE

```
/home/user/mcnp-skills/
├── AGENT8_FILL_ARRAY_DEEP_DIVE.md
├── AGR1_CELL_CARD_COMPLETE_ANALYSIS.md
├── AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md
├── AGR1_Material_Card_Analysis.md
├── AGR1_TEMPLATE_STRUCTURE_ANALYSIS.md
├── ANALYSIS_INPUT_GENERATION_WORKFLOW.md
├── HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md
├── COMPREHENSIVE_FINDINGS_SYNTHESIS.md
├── SKILL_REFINEMENT_PLAN_EXECUTABLE_REVISED.md
├── EXECUTION_SUMMARY_NEXT_SESSION_REVISED.md
├── analysis_reports/
│   ├── AGENT9_CROSS_REFERENCING_PATTERNS.md
│   ├── AGENT9_QUICK_REFERENCE.md
│   ├── AGENT9_VISUAL_DIAGRAMS.md
│   └── README_AGENT9.md
└── example_files/reactor-model_examples/htgr-model-burnup-and-doserates/
    ├── AGR-1_Technical_Analysis_Report.md
    └── QUICK_REFERENCE_TRISO_SPECS.md
```

---

## ✅ CORRECT FILE PATHS

### Root Level (`/home/user/mcnp-skills/`)

```bash
/home/user/mcnp-skills/AGENT8_FILL_ARRAY_DEEP_DIVE.md
/home/user/mcnp-skills/AGR1_CELL_CARD_COMPLETE_ANALYSIS.md
/home/user/mcnp-skills/AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md
/home/user/mcnp-skills/AGR1_Material_Card_Analysis.md
/home/user/mcnp-skills/AGR1_TEMPLATE_STRUCTURE_ANALYSIS.md
/home/user/mcnp-skills/ANALYSIS_INPUT_GENERATION_WORKFLOW.md
/home/user/mcnp-skills/HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md
/home/user/mcnp-skills/COMPREHENSIVE_FINDINGS_SYNTHESIS.md
```

### Analysis Reports Subdirectory

```bash
/home/user/mcnp-skills/analysis_reports/AGENT9_CROSS_REFERENCING_PATTERNS.md
/home/user/mcnp-skills/analysis_reports/AGENT9_QUICK_REFERENCE.md
/home/user/mcnp-skills/analysis_reports/AGENT9_VISUAL_DIAGRAMS.md
/home/user/mcnp-skills/analysis_reports/README_AGENT9.md
```

### Example Files Subdirectory

```bash
/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/AGR-1_Technical_Analysis_Report.md
/home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/QUICK_REFERENCE_TRISO_SPECS.md
```

---

## ⚠️ COMMON MISTAKES

### ❌ WRONG Paths (DO NOT USE)

```bash
# Agent 9 documents are NOT at root
❌ /home/user/mcnp-skills/AGENT9_CROSS_REFERENCING_PATTERNS.md
❌ /home/user/mcnp-skills/AGENT9_QUICK_REFERENCE.md

# AGR-1 analysis is NOT at root
❌ /home/user/mcnp-skills/AGR-1_Technical_Analysis_Report.md
```

### ✅ CORRECT Paths

```bash
# Agent 9 documents ARE in analysis_reports/
✅ /home/user/mcnp-skills/analysis_reports/AGENT9_CROSS_REFERENCING_PATTERNS.md
✅ /home/user/mcnp-skills/analysis_reports/AGENT9_QUICK_REFERENCE.md

# AGR-1 analysis IS in example_files subdirectory
✅ /home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/AGR-1_Technical_Analysis_Report.md
```

---

## 📊 DOCUMENT METADATA

| Document | Size | Location | Primary Use |
|----------|------|----------|-------------|
| AGENT8_FILL_ARRAY_DEEP_DIVE.md | 46 KB | Root | Lattice building |
| AGR1_CELL_CARD_COMPLETE_ANALYSIS.md | 31 KB | Root | Cell patterns |
| AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md | 39 KB | Root | Surface patterns |
| AGR1_Material_Card_Analysis.md | 46 KB | Root | Material patterns |
| AGR1_TEMPLATE_STRUCTURE_ANALYSIS.md | 50 KB | Root | Template automation |
| ANALYSIS_INPUT_GENERATION_WORKFLOW.md | 50 KB | Root | Programmatic generation |
| HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md | 39 KB | Root | Best practices |
| COMPREHENSIVE_FINDINGS_SYNTHESIS.md | 28 KB | Root | Overall synthesis |
| AGENT9_CROSS_REFERENCING_PATTERNS.md | 45 KB | analysis_reports/ | Cross-references |
| AGENT9_QUICK_REFERENCE.md | 8.7 KB | analysis_reports/ | Quick lookup |
| AGENT9_VISUAL_DIAGRAMS.md | 37 KB | analysis_reports/ | Diagrams |
| README_AGENT9.md | 11 KB | analysis_reports/ | Agent 9 overview |
| AGR-1_Technical_Analysis_Report.md | 58 KB | example_files/.../htgr.../ | TRISO specs |
| QUICK_REFERENCE_TRISO_SPECS.md | 20 KB | example_files/.../htgr.../ | Quick TRISO ref |

**Total**: 469 KB of comprehensive analysis

---

## 🔍 VERIFICATION COMMANDS

To verify file locations:

```bash
# Check root level
ls -lh /home/user/mcnp-skills/AGENT*.md
ls -lh /home/user/mcnp-skills/AGR1*.md
ls -lh /home/user/mcnp-skills/HTGR*.md

# Check analysis_reports/
ls -lh /home/user/mcnp-skills/analysis_reports/

# Check example_files/
ls -lh /home/user/mcnp-skills/example_files/reactor-model_examples/htgr-model-burnup-and-doserates/

# Find all analysis documents
find /home/user/mcnp-skills -name "*.md" -type f | grep -E "(AGENT|AGR1|HTGR|ANALYSIS)" | sort
```

---

## 📋 SKILL → DOCUMENT MAPPING

### mcnp-lattice-builder
- PRIMARY: `AGENT8_FILL_ARRAY_DEEP_DIVE.md` (root)
- `AGR1_CELL_CARD_COMPLETE_ANALYSIS.md` (root)
- `AGR1_SURFACE_CARD_COMPLETE_ANALYSIS.md` (root)
- `COMPREHENSIVE_FINDINGS_SYNTHESIS.md` (root)

### mcnp-material-builder
- PRIMARY: `AGR1_Material_Card_Analysis.md` (root)
- `AGR-1_Technical_Analysis_Report.md` (example_files/.../htgr.../)
- `QUICK_REFERENCE_TRISO_SPECS.md` (example_files/.../htgr.../)
- `COMPREHENSIVE_FINDINGS_SYNTHESIS.md` (root)

### mcnp-input-validator
- PRIMARY: `AGENT9_CROSS_REFERENCING_PATTERNS.md` (analysis_reports/)
- `AGENT8_FILL_ARRAY_DEEP_DIVE.md` (root)
- `AGR1_CELL_CARD_COMPLETE_ANALYSIS.md` (root)
- `COMPREHENSIVE_FINDINGS_SYNTHESIS.md` (root)

### mcnp-cross-reference-checker
- PRIMARY: `AGENT9_CROSS_REFERENCING_PATTERNS.md` (analysis_reports/)
- `AGENT9_QUICK_REFERENCE.md` (analysis_reports/)
- `AGENT9_VISUAL_DIAGRAMS.md` (analysis_reports/)
- `README_AGENT9.md` (analysis_reports/)
- `COMPREHENSIVE_FINDINGS_SYNTHESIS.md` (root)

### mcnp-template-generator
- PRIMARY: `AGR1_TEMPLATE_STRUCTURE_ANALYSIS.md` (root)
- PRIMARY: `ANALYSIS_INPUT_GENERATION_WORKFLOW.md` (root)
- `COMPREHENSIVE_FINDINGS_SYNTHESIS.md` (root)

### mcnp-programmatic-generator
- PRIMARY: `ANALYSIS_INPUT_GENERATION_WORKFLOW.md` (root)
- `AGR1_TEMPLATE_STRUCTURE_ANALYSIS.md` (root)
- `COMPREHENSIVE_FINDINGS_SYNTHESIS.md` (root)

### mcnp-workflow-integrator
- PRIMARY: `HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md` (root)
- `COMPREHENSIVE_FINDINGS_SYNTHESIS.md` (root)

### mcnp-best-practices-checker
- PRIMARY: `HTGR_MODEL_BEST_PRACTICES_SYNTHESIS.md` (root)
- `AGENT9_CROSS_REFERENCING_PATTERNS.md` (analysis_reports/)
- `COMPREHENSIVE_FINDINGS_SYNTHESIS.md` (root)

---

**Use this document** to ensure all file paths are correct when implementing refinement plans!

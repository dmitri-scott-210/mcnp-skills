# MCNP Workflow Orchestration Examples

**Architecture**: Main Claude intelligently orchestrates specialist agents
**Status**: Active as of 2025-11-05
**Version**: 2.0 (revised from 3-tier to 2-tier)

---

## How It Works

When you give me a request, I:

1. **Analyze** what you need (validation? building? analysis? optimization?)
2. **Select** appropriate specialist agents based on context
3. **Invoke** specialists sequentially or in parallel via Task tool
4. **Synthesize** results from all specialists into comprehensive report
5. **Pass context** between specialists in multi-step workflows

---

## Example Workflows

### Workflow 1: Simple Validation

**Your Request**:
```
"Validate reactor.inp"
```

**My Orchestration**:
```
Step 1: Analyze request → Need input validation
Step 2: Invoke specialist
  → Task(subagent_type="mcnp-input-validator",
         prompt="Validate reactor.inp for syntax, format, cross-references")
Step 3: Receive report from specialist
Step 4: Present findings to you
```

**Result**: Validation report with errors, warnings, recommendations

---

### Workflow 2: Benchmark Validation (Complex)

**Your Request**:
```
"Validate msre-model-v1.inp against the Berkeley benchmark paper"
```

**My Orchestration**:
```
Step 1: Analyze request → Need benchmark specs + comprehensive validation
Step 2: Invoke documentation analyst
  → Task(subagent_type="mcnp-tech-doc-analyzer",
         prompt="Extract benchmark specifications from msre-benchmark-berkeley.md:
                 - Expected geometry dimensions
                 - Material compositions
                 - Expected keff = 0.99978 ± 420 pcm
                 - Known modeling simplifications")
Step 3: Receive benchmark specifications
Step 4: Invoke 3 validators IN PARALLEL (single message, multiple Task calls)
  → Task(subagent_type="mcnp-input-validator", ...)
  → Task(subagent_type="mcnp-geometry-checker",
         context="Benchmark specs: core radius 70.285 cm, height 170.311 cm...")
  → Task(subagent_type="mcnp-cross-reference-checker", ...)
Step 5: Receive all 3 validation reports
Step 6: Synthesize comprehensive benchmark validation report
  - Compare geometry against specs
  - Check material compositions match benchmark
  - Identify deviations and estimate bias
Step 7: Present findings to you
```

**Result**: Benchmark compliance report with spec comparisons

---

### Workflow 3: Build from Technical Paper

**Your Request**:
```
"Build an MCNP model of the MSRE reactor from ORNL-4528"
```

**My Orchestration**:
```
Step 1: Analyze request → Need doc extraction + geometry building + materials + validation
Step 2: Invoke documentation analyst
  → Task(subagent_type="mcnp-tech-doc-analyzer",
         prompt="Extract from ORNL-4528:
                 - Core geometry specifications (dimensions, lattice arrangement)
                 - Graphite stringer dimensions
                 - Fuel salt composition
                 - Control rod specifications
                 - Vessel geometry")
Step 3: Receive extracted specifications
Step 4: Invoke geometry builder
  → Task(subagent_type="mcnp-geometry-builder",
         prompt="Build MSRE geometry using specifications:
                 Core radius: 70.285 cm
                 Height: 170.311 cm
                 Lattice: 28×28 array of 5.08×5.08 cm stringers
                 Channel dimensions: 1.016 × 3.048 cm
                 [... full specs from Step 3]")
Step 5: Receive geometry cards
Step 6: Invoke material builder
  → Task(subagent_type="mcnp-material-builder",
         prompt="Create materials:
                 M1: Fuel salt (LiF-BeF2-ZrF4-UF4)
                     Li: 10.957 wt%, Be: 6.349 wt%, ...
                     Density: 2.3275 g/cm³
                     Temperature: 911 K
                 M2: Graphite
                     Density: 1.86 g/cm³
                     [... full compositions from Step 3]")
Step 7: Receive material cards
Step 8: Combine geometry + materials + add physics/source/tallies
Step 9: Invoke validator to check
  → Task(subagent_type="mcnp-input-validator",
         prompt="Validate complete input file")
Step 10: Receive validation report
Step 11: Present complete input file + validation report to you
```

**Result**: Complete MCNP input file with documentation of sources

---

### Workflow 4: Optimization Pipeline

**Your Request**:
```
"This deep penetration shielding problem has terrible statistics.
Optimize it with variance reduction."
```

**My Orchestration**:
```
Step 1: Analyze request → Need VR analysis + optimization + implementation
Step 2: Invoke input validator (ensure starting point is valid)
  → Task(subagent_type="mcnp-input-validator", ...)
Step 3: If valid, invoke variance reducer
  → Task(subagent_type="mcnp-variance-reducer",
         prompt="Analyze shielding-problem.inp:
                 - Identify geometry characteristics (thick shield? streaming paths?)
                 - Determine optimal VR techniques
                 - Recommend weight window strategy
                 - Estimate expected FOM improvement")
Step 4: Receive VR analysis and recommendations
Step 5: Invoke weight window optimizer
  → Task(subagent_type="mcnp-ww-optimizer",
         prompt="Generate weight windows for shielding-problem.inp:
                 - Use mesh-based WWG approach
                 - Energy groups: [from VR analysis]
                 - Detector location: [from problem]
                 - Generate WWN/WWE cards")
Step 6: Receive weight window specification
Step 7: Invoke input editor to apply VR
  → Task(subagent_type="mcnp-input-editor",
         prompt="Add to shielding-problem.inp:
                 - Weight window cards [from Step 6]
                 - Adjust source biasing if recommended
                 - Update CUT cards if needed")
Step 8: Receive modified input
Step 9: Invoke validator to verify optimized input
  → Task(subagent_type="mcnp-input-validator", ...)
Step 10: Present optimized input + expected performance improvement
```

**Result**: VR-optimized input file with estimated FOM improvement

---

### Workflow 5: Error Debugging

**Your Request**:
```
"MCNP crashed with 'fatal error: surface 214 has not been defined'.
Here's the output file. Fix it."
```

**My Orchestration**:
```
Step 1: Analyze request → Need error diagnosis + fix
Step 2: Invoke output parser
  → Task(subagent_type="mcnp-output-parser",
         prompt="Parse mcnp_output.txt and extract:
                 - All fatal errors
                 - Location in input file
                 - Problematic cards")
Step 3: Receive parsed error information
Step 4: Invoke fatal error debugger
  → Task(subagent_type="mcnp-fatal-error-debugger",
         prompt="Diagnose and fix: 'surface 214 has not been defined'
                 Context: Referenced in cells 11,12,13 (control rod universe)
                 Provide: Corrected surface definitions")
Step 5: Receive diagnosis and fix
Step 6: If geometry error, invoke geometry checker
  → Task(subagent_type="mcnp-geometry-checker",
         prompt="Verify corrected geometry has no overlaps/gaps")
Step 7: Invoke cross-reference checker
  → Task(subagent_type="mcnp-cross-reference-checker",
         prompt="Verify all surface references are now defined")
Step 8: Present corrected input file with explanation
```

**Result**: Fixed input file with explanation of error and fix

---

### Workflow 6: Results Analysis

**Your Request**:
```
"Analyze my KCODE run. Is it converged? What's the keff?"
```

**My Orchestration**:
```
Step 1: Analyze request → Need output parsing + statistics check + criticality analysis
Step 2: Invoke output parser
  → Task(subagent_type="mcnp-output-parser",
         prompt="Parse mcnp_output.txt:
                 - Extract keff values (KCODE cycles)
                 - Extract entropy
                 - Extract source convergence data")
Step 3: Receive parsed data
Step 4: Invoke statistics checker AND criticality analyzer IN PARALLEL
  → Task(subagent_type="mcnp-statistics-checker",
         prompt="Check convergence of keff:
                 - Apply 10 statistical tests
                 - Check source convergence
                 - Verify active/skip cycles adequate")
  → Task(subagent_type="mcnp-criticality-analyzer",
         prompt="Analyze KCODE results:
                 - keff value and uncertainty
                 - Entropy convergence
                 - Confidence in result")
Step 5: Receive both analysis reports
Step 6: If plots requested, invoke plotter
  → Task(subagent_type="mcnp-plotter",
         prompt="Generate plots:
                 - keff vs cycle
                 - Shannon entropy vs cycle")
Step 7: Synthesize comprehensive analysis
  - keff result
  - Convergence assessment
  - Confidence level
  - Recommendations (if under-converged)
Step 8: Present analysis report
```

**Result**: Complete criticality analysis with convergence assessment

---

## Key Advantages of This Architecture

### 1. Context Preservation
I maintain full conversation history, so specialists benefit from:
- Previous analysis results
- User preferences
- Project-specific details

### 2. Intelligent Routing
I decide which specialists to invoke based on:
- Request type
- File contents
- Previous specialist findings

### 3. Adaptive Workflows
I adjust the workflow based on intermediate results:
- If validator finds errors → invoke error debugger
- If geometry is complex → invoke geometry checker
- If optimization is needed → chain VR specialists

### 4. Parallel Execution
I can invoke multiple specialists simultaneously:
- 3-4 validators in parallel for comprehensive checks
- Parser + statistics checker + analyzer in parallel
- Faster results when tasks are independent

### 5. Result Synthesis
I combine specialist reports into coherent narratives:
- Remove redundancies
- Highlight key findings
- Provide actionable recommendations

---

## Specialist Agent Catalog (Current)

### Validation Category
1. ✅ **mcnp-input-validator** - Syntax, format, block structure
2. ✅ **mcnp-geometry-checker** - Geometry validation, overlaps, gaps
3. ✅ **mcnp-cross-reference-checker** - Cell→surface, cell→material references
4. ⏳ mcnp-physics-validator - Physics settings, MODE, cross-sections
5. ⏳ mcnp-cell-checker - Universe/LAT/FILL validation
6. ⏳ mcnp-fatal-error-debugger - Fatal error diagnosis
7. ⏳ mcnp-warning-analyzer - Warning interpretation
8. ⏳ mcnp-best-practices-checker - Best practices compliance
9. ⏳ mcnp-statistics-checker - Statistical convergence

### Reference Category
1. ✅ **mcnp-tech-doc-analyzer** - Technical paper/report analysis
2. ⏳ mcnp-isotope-lookup - ZAID, isotopic data
3. ⏳ mcnp-cross-section-manager - Cross-section library management
4. ⏳ mcnp-physical-constants - Physical constants lookup
5. ⏳ mcnp-example-finder - Example file finder
6. ⏳ mcnp-knowledge-docs-finder - Documentation search

### Building Category (Future)
- mcnp-input-builder, mcnp-geometry-builder, mcnp-material-builder,
- mcnp-source-builder, mcnp-tally-builder, mcnp-physics-builder,
- mcnp-lattice-builder, mcnp-mesh-builder, mcnp-burnup-builder,
- mcnp-template-generator

### Editing Category (Future)
- mcnp-input-editor, mcnp-geometry-editor,
- mcnp-transform-editor, mcnp-unit-converter

### Analysis Category (Future)
- mcnp-output-parser, mcnp-mctal-processor, mcnp-tally-analyzer,
- mcnp-criticality-analyzer, mcnp-plotter

### Optimization Category (Future)
- mcnp-variance-reducer, mcnp-ww-optimizer

---

## How to Request Workflows

### Simple Requests
Just tell me what you need:
- "Validate this input file"
- "Extract geometry from this paper"
- "Fix these errors"

I'll automatically select and chain the right specialists.

### Explicit Workflow Requests
You can specify the workflow if you want:
- "First extract specs from the paper, then build geometry, then validate"
- "Analyze the output, check statistics, and generate plots"
- "Validate geometry, check cross-references, and assess best practices"

I'll follow your specified workflow and add any missing steps if needed.

### Complex Requests
For complex tasks, I'll break them down:
- "Build a complete benchmark model from this paper"
  → I'll orchestrate: doc analysis → geometry → materials → physics → validation
- "Optimize this problem and validate the result"
  → I'll orchestrate: validate input → VR analysis → WW generation → editing → revalidate

---

## Testing Status

**Tested Workflows** (as of 2025-11-05):
- ✅ Single specialist invocation (mcnp-validation-lead)
- ✅ Specialist uses embedded expertise (9/10 quality)
- ✅ Comprehensive validation report generation
- ⏳ Parallel specialist invocation (not yet tested)
- ⏳ Sequential workflow chaining (not yet tested)
- ⏳ Documentation → validation workflow (not yet tested)

**Next Tests**:
1. Invoke 3 validators in parallel
2. Chain doc-analyzer → geometry-builder → validator
3. Error debugging workflow (parser → debugger → fixer)

---

**This document will be updated as new specialists are created and workflows are tested.**

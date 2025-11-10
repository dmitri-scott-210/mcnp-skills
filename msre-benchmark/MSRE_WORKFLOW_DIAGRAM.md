# MSRE Workflow Visual Diagrams
## Integration Patterns and Data Flow

---

## OVERALL WORKFLOW ARCHITECTURE

```
╔═══════════════════════════════════════════════════════════════════════╗
║                          PHASE 1: LITERATURE ANALYSIS                 ║
╚═══════════════════════════════════════════════════════════════════════╝
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
        ┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
        │ Tech-Doc-Analyzer│ │ Tech-Doc-   │ │ Tech-Doc-       │
        │   Instance 1    │ │  Analyzer   │ │  Analyzer       │
        │  (Berkeley)     │ │ Instance 2  │ │  Instance 3     │
        │                 │ │ (Design)    │ │ (Additional)    │
        └─────────────────┘ └─────────────┘ └─────────────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                            ┌───────────────┐
                            │    CLAUDE     │
                            │ Consolidation │
                            └───────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            [Unit Converter] [Isotope Lookup] [Physical Constants]
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                        [Design Specification Document]
                                    │
╔═══════════════════════════════════════════════════════════════════════╗
║                    PHASE 2: MODEL DEVELOPMENT                         ║
╚═══════════════════════════════════════════════════════════════════════╝
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
            [Geometry Planning]              [Lattice Planning]
          (mcnp-geometry-builder)        (mcnp-lattice-builder)
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
                            ┌───────────────┐
                            │    CLAUDE     │
                            │   Strategy    │
                            │   Approval    │
                            └───────────────┘
                                    │
╔═══════════════════════════════════════════════════════════════════════╗
║                      LATTICE CONSTRUCTION LOOP                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║   ┌─────────────────┐         ┌─────────────────┐                   ║
║   │ Lattice Builder │────────▶│ Geometry Builder│                   ║
║   │     (Agent)     │         │     (Skill)     │                   ║
║   │   BUILD LATTICE │         │  REVIEW SYNTAX  │                   ║
║   └─────────────────┘         └─────────────────┘                   ║
║           │                            │                             ║
║           │                            ▼                             ║
║           │                   ┌─────────────────┐                   ║
║           │                   │  Cell Checker   │                   ║
║           │                   │     (Agent)     │                   ║
║           │                   │  VALIDATE REFS  │                   ║
║           │                   └─────────────────┘                   ║
║           │                            │                             ║
║           │                            ▼                             ║
║           │                      [Issues Found?]                     ║
║           │                            │                             ║
║           │                     YES ◄──┴──► NO                       ║
║           │                      │           │                       ║
║           └──────────────────────┘           ▼                       ║
║                 (ITERATE)              [PROCEED]                     ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
        ┌─────────────────────┐       ┌─────────────────────┐
        │ Reflector Building  │       │  Vessel Building    │
        │  (Geometry Skill)   │       │  (Geometry Skill)   │
        │     PARALLEL        │       │     PARALLEL        │
        └─────────────────────┘       └─────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
╔═══════════════════════════════════════════════════════════════════════╗
║                      MATERIAL CONSTRUCTION (PARALLEL)                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            ║
║  │Material  │  │Material  │  │Material  │  │Material  │            ║
║  │Builder 1 │  │Builder 2 │  │Builder 3 │  │Builder 4 │            ║
║  │(Fuel)    │  │(Graphite)│  │(Hastelloy)│  │(Control) │            ║
║  └──────────┘  └──────────┘  └──────────┘  └──────────┘            ║
║       │             │             │             │                    ║
║       └─────────────┴─────────────┴─────────────┘                    ║
║                          │                                            ║
║                          ▼                                            ║
║              ┌─────────────────────────┐                             ║
║              │ Cross-Section Manager   │                             ║
║              │   (Verify all ZAIDs)    │                             ║
║              └─────────────────────────┘                             ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │    Source + Physics       │
                    │  (Source/Physics Skills)  │
                    └───────────────────────────┘
                                    │
╔═══════════════════════════════════════════════════════════════════════╗
║                   VALIDATION CASCADE (SEQUENTIAL)                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║                    ┌─────────────────────┐                           ║
║                    │  Input Validator    │                           ║
║                    │ (Syntax & Format)   │                           ║
║                    └─────────────────────┘                           ║
║                             │ PASS                                    ║
║                             ▼                                         ║
║                    ┌─────────────────────┐                           ║
║                    │ Geometry Checker    │                           ║
║                    │ (Overlaps & Gaps)   │                           ║
║                    └─────────────────────┘                           ║
║                             │ PASS                                    ║
║                             ▼                                         ║
║                    ┌─────────────────────┐                           ║
║                    │Cross-Ref Checker    │                           ║
║                    │ (All References)    │                           ║
║                    └─────────────────────┘                           ║
║                             │ PASS                                    ║
║                             ▼                                         ║
║                    ┌─────────────────────┐                           ║
║                    │Best Practices Check │                           ║
║                    │   (57 Items)        │                           ║
║                    └─────────────────────┘                           ║
║                             │ PASS                                    ║
║                             ▼                                         ║
║                    ┌─────────────────────┐                           ║
║                    │  Physics Validator  │                           ║
║                    │ (MODE/PHYS/Libs)    │                           ║
║                    └─────────────────────┘                           ║
║                             │ PASS                                    ║
║                             ▼                                         ║
║                      ┌─────────────┐                                 ║
║                      │   CLAUDE    │                                 ║
║                      │  GATE 2     │                                 ║
║                      │  APPROVAL   │                                 ║
║                      └─────────────┘                                 ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
                                    │
                                    ▼
╔═══════════════════════════════════════════════════════════════════════╗
║                       MCNP EXECUTION & DEBUG                          ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║                    ┌─────────────────────┐                           ║
║                    │   RUN MCNP          │                           ║
║                    │ (Geometry Plot Mode)│                           ║
║                    └─────────────────────┘                           ║
║                             │                                         ║
║                    ┌────────┴────────┐                               ║
║                    ▼                 ▼                                ║
║            [Fatal Error?]      [Success]                             ║
║                    │                 │                                ║
║                YES │                 │ NO                             ║
║                    ▼                 │                                ║
║        ┌─────────────────────┐      │                               ║
║        │ Fatal Error Debugger│      │                               ║
║        │   (Agent)           │      │                               ║
║        └─────────────────────┘      │                               ║
║                    │                 │                                ║
║                    ▼                 │                                ║
║                [FIX INPUT]           │                               ║
║                    │                 │                                ║
║                    └────────┬────────┘                               ║
║                             │                                         ║
║                             ▼                                         ║
║                    ┌─────────────────────┐                           ║
║                    │   RUN MCNP          │                           ║
║                    │   (Full Run)        │                           ║
║                    └─────────────────────┘                           ║
║                             │                                         ║
║                    ┌────────┴────────┐                               ║
║                    ▼                 ▼                                ║
║             [Warnings?]          [Clean]                             ║
║                    │                 │                                ║
║                YES │                 │ NO                             ║
║                    ▼                 │                                ║
║        ┌─────────────────────┐      │                               ║
║        │ Warning Analyzer    │      │                               ║
║        │   (Agent)           │      │                               ║
║        └─────────────────────┘      │                               ║
║                    │                 │                                ║
║                    └────────┬────────┘                               ║
║                             │                                         ║
║                             ▼                                         ║
║                    ┌─────────────────────┐                           ║
║                    │  Output Parser      │                           ║
║                    │    (Agent)          │                           ║
║                    └─────────────────────┘                           ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
                                    │
╔═══════════════════════════════════════════════════════════════════════╗
║                   RESULTS ANALYSIS (PARALLEL)                         ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     ║
║  │  Criticality    │  │   Statistics    │  │     Plotter     │     ║
║  │    Analyzer     │  │     Checker     │  │      (Skill)    │     ║
║  │   (Agent)       │  │    (Agent)      │  │                 │     ║
║  │                 │  │                 │  │                 │     ║
║  │ • keff ± σ     │  │ • 10 checks     │  │ • XY plots      │     ║
║  │ • Entropy       │  │ • FOM           │  │ • XZ plots      │     ║
║  │ • Source dist   │  │ • Confidence    │  │ • YZ plots      │     ║
║  │ • C-E calc      │  │   intervals     │  │ • Convergence   │     ║
║  └─────────────────┘  └─────────────────┘  └─────────────────┘     ║
║           │                   │                     │                ║
║           └───────────────────┴─────────────────────┘                ║
║                               │                                       ║
║                               ▼                                       ║
║                      ┌─────────────────┐                             ║
║                      │     CLAUDE      │                             ║
║                      │   Synthesize    │                             ║
║                      │     Report      │                             ║
║                      └─────────────────┘                             ║
║                               │                                       ║
║                               ▼                                       ║
║                        ┌─────────────┐                               ║
║                        │   GATE 3    │                               ║
║                        │  Phase 1    │                               ║
║                        │  Complete?  │                               ║
║                        └─────────────┘                               ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
                                    │
╔═══════════════════════════════════════════════════════════════════════╗
║                  PHASE 3: BENCHMARK REFINEMENT                        ║
╚═══════════════════════════════════════════════════════════════════════╝
                                    │
                                    ▼
                    ┌──────────────────────────┐
                    │  Tech-Doc-Analyzer       │
                    │  (Re-analyze Benchmark)  │
                    └──────────────────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │    CLAUDE     │
                            │   Compare     │
                            │ Phase1 vs     │
                            │  Benchmark    │
                            └───────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
        ┌─────────────────────┐       ┌─────────────────────┐
        │ Geometry Editor     │       │  Material Builder   │
        │  (Refinements)      │       │  (Refinements)      │
        └─────────────────────┘       └─────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
                    ┌──────────────────────────┐
                    │   Physics Builder        │
                    │  (Benchmark Settings)    │
                    └──────────────────────────┘
                                    │
                                    ▼
                [REPEAT VALIDATION CASCADE]
                                    │
                                    ▼
                            ┌───────────────┐
                            │   GATE 4      │
                            │  Benchmark    │
                            │  Run Approval │
                            └───────────────┘
                                    │
                                    ▼
                        [MCNP BENCHMARK RUN]
                                    │
                                    ▼
                    [RESULTS ANALYSIS (Parallel)]
                                    │
                                    ▼
                            ┌───────────────┐
                            │   GATE 5      │
                            │  Validation   │
                            │   Success     │
                            └───────────────┘

```

---

## INTEGRATION PATTERN DETAILS

### Pattern 1: Sequential Cascade

```
┌──────────────────────────────────────────────────┐
│ VALIDATION CASCADE (Step 2.6)                    │
├──────────────────────────────────────────────────┤
│                                                  │
│  Agent 1 (Input Validator)                      │
│       │                                          │
│       ├─── PASS? ──── NO ──► [STOP & FIX]       │
│       │                                          │
│       └─── YES                                   │
│              ▼                                   │
│  Agent 2 (Geometry Checker)                     │
│       │                                          │
│       ├─── PASS? ──── NO ──► [STOP & FIX]       │
│       │                                          │
│       └─── YES                                   │
│              ▼                                   │
│  Agent 3 (Cross-Ref Checker)                    │
│       │                                          │
│       ├─── PASS? ──── NO ──► [STOP & FIX]       │
│       │                                          │
│       └─── YES                                   │
│              ▼                                   │
│  Agent 4 (Best Practices)                       │
│       │                                          │
│       ├─── PASS? ──── NO ──► [STOP & FIX]       │
│       │                                          │
│       └─── YES                                   │
│              ▼                                   │
│  Agent 5 (Physics Validator)                    │
│       │                                          │
│       └─── PASS? ──── YES ──► [PROCEED]         │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Key Feature:** Each stage gates the next. Early failure stops cascade.

---

### Pattern 2: Parallel Execution

```
┌────────────────────────────────────────────────────────┐
│ MATERIAL BUILDING (Step 2.4)                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│                  ┌─────────────────┐                  │
│                  │     CLAUDE      │                  │
│                  │   Coordinates   │                  │
│                  └─────────────────┘                  │
│                          │                             │
│          ┌───────────────┼───────────────┬─────────┐  │
│          │               │               │         │  │
│          ▼               ▼               ▼         ▼  │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐ ┌────┐│
│  │ Material   │  │ Material   │  │ Material │ │Mat ││
│  │ Builder 1  │  │ Builder 2  │  │ Builder 3│ │ 4  ││
│  │            │  │            │  │          │ │    ││
│  │ Fuel Salt  │  │ Graphite   │  │ Hastelloy│ │Ctrl││
│  │            │  │            │  │          │ │    ││
│  │ Working... │  │ Working... │  │ Working..│ │... ││
│  └────────────┘  └────────────┘  └──────────┘ └────┘│
│          │               │               │         │  │
│          └───────────────┼───────────────┴─────────┘  │
│                          │                             │
│                          ▼                             │
│                  ┌─────────────────┐                  │
│                  │     CLAUDE      │                  │
│                  │  Consolidates   │                  │
│                  │  All Materials  │                  │
│                  └─────────────────┘                  │
│                          │                             │
│                          ▼                             │
│               ┌─────────────────────┐                 │
│               │ Cross-Section Mgr   │                 │
│               │  Verifies All       │                 │
│               └─────────────────────┘                 │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**Key Feature:** All instances run simultaneously. Claude waits for all to complete.

---

### Pattern 3: Validation Loop

```
┌───────────────────────────────────────────────────┐
│ LATTICE CONSTRUCTION LOOP (Step 2.2)              │
├───────────────────────────────────────────────────┤
│                                                   │
│   START                                           │
│     │                                             │
│     ▼                                             │
│  ┌────────────────────┐                          │
│  │ Lattice Builder    │ ◄─────────┐              │
│  │    (Agent)         │           │              │
│  │                    │           │              │
│  │ Build lattice      │           │              │
│  │ structure          │           │              │
│  └────────────────────┘           │              │
│           │                        │              │
│           ▼                        │              │
│  ┌────────────────────┐           │              │
│  │ Geometry Builder   │           │              │
│  │    (Skill)         │           │              │
│  │                    │           │ ITERATE      │
│  │ Review syntax      │           │ & FIX        │
│  │ Check formatting   │           │              │
│  └────────────────────┘           │              │
│           │                        │              │
│           ▼                        │              │
│  ┌────────────────────┐           │              │
│  │  Cell Checker      │           │              │
│  │    (Agent)         │           │              │
│  │                    │           │              │
│  │ Validate U/FILL    │           │              │
│  │ Check LAT specs    │           │              │
│  │ Verify dimensions  │           │              │
│  └────────────────────┘           │              │
│           │                        │              │
│           ▼                        │              │
│      [Issues Found?]               │              │
│           │                        │              │
│     ┌─────┴─────┐                 │              │
│     │           │                  │              │
│    YES         NO                  │              │
│     │           │                  │              │
│     ├───────────┘                  │              │
│     │                              │              │
│     └──────────────────────────────┘              │
│                                                   │
│    [PROCEED TO NEXT STEP]                        │
│                                                   │
└───────────────────────────────────────────────────┘
```

**Key Feature:** Continuous iteration until validation passes. No proceed until clean.

---

### Pattern 4: Skill-Agent Handoff

```
┌──────────────────────────────────────────────┐
│ GEOMETRY TO VALIDATION (Step 2.3 → 2.6)     │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────────────┐                     │
│  │ Geometry Builder   │ (SKILL)             │
│  │                    │                     │
│  │ • Build reflector  │                     │
│  │ • Build vessel     │                     │
│  │ • Define cells     │                     │
│  └────────────────────┘                     │
│           │                                  │
│           │ [Output: Cell definitions]      │
│           ▼                                  │
│  ┌────────────────────┐                     │
│  │      CLAUDE        │                     │
│  │                    │                     │
│  │ • Reviews output   │                     │
│  │ • Sanity checks    │                     │
│  │ • Prepares context │                     │
│  └────────────────────┘                     │
│           │                                  │
│           │ [Context + instructions]        │
│           ▼                                  │
│  ┌────────────────────┐                     │
│  │ Geometry Checker   │ (AGENT)             │
│  │                    │                     │
│  │ • Check overlaps   │                     │
│  │ • Find gaps        │                     │
│  │ • Validate Boolean │                     │
│  └────────────────────┘                     │
│           │                                  │
│           │ [Validation report]              │
│           ▼                                  │
│  ┌────────────────────┐                     │
│  │      CLAUDE        │                     │
│  │                    │                     │
│  │ • Approves/rejects │                     │
│  │ • Gates next step  │                     │
│  └────────────────────┘                     │
│                                              │
└──────────────────────────────────────────────┘
```

**Key Feature:** Skill does fast execution, Agent does deep validation, Claude mediates.

---

### Pattern 5: Agent-Skill Handoff

```
┌──────────────────────────────────────────────┐
│ PLANNING TO EXECUTION (Step 2.1 → 2.2)      │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────────────┐                     │
│  │ Lattice Builder    │ (AGENT - Planning)  │
│  │                    │                     │
│  │ • Research lattice │                     │
│  │   strategies       │                     │
│  │ • Analyze examples │                     │
│  │ • Design hierarchy │                     │
│  │ • Plan indexing    │                     │
│  └────────────────────┘                     │
│           │                                  │
│           │ [Output: Lattice strategy doc]  │
│           ▼                                  │
│  ┌────────────────────┐                     │
│  │      CLAUDE        │                     │
│  │                    │                     │
│  │ • Reviews strategy │                     │
│  │ • Approves plan    │                     │
│  │ • Converts to      │                     │
│  │   build tasks      │                     │
│  └────────────────────┘                     │
│           │                                  │
│           │ [Approved build instructions]   │
│           ▼                                  │
│  ┌────────────────────┐                     │
│  │ Geometry Builder   │ (SKILL - Execution) │
│  │                    │                     │
│  │ • Execute plan     │                     │
│  │ • Build quickly    │                     │
│  │ • Create cells     │                     │
│  └────────────────────┘                     │
│           │                                  │
│           │ [Built geometry]                 │
│           ▼                                  │
│         [Next step]                          │
│                                              │
└──────────────────────────────────────────────┘
```

**Key Feature:** Agent researches/plans (token-intensive), Skill executes (token-efficient).

---

## TOKEN FLOW VISUALIZATION

```
┌─────────────────────────────────────────────────────────────┐
│               TOKEN USAGE BY WORKFLOW PHASE                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1: Literature Analysis                              │
│  ████████████████████                    ~50K tokens       │
│  │                                                          │
│  ├─ Tech-Doc-Analyzer × 3 (parallel)     40K               │
│  ├─ Example Finder                        5K               │
│  └─ Claude + Skills                       5K               │
│                                                             │
│  Phase 2: Model Development                                │
│  ██████████████████████████████████████  ~200K tokens      │
│  │                                                          │
│  ├─ Planning Agents (2)                  15K               │
│  ├─ Construction Loop                    30K               │
│  ├─ Material Builders (4 parallel)       20K               │
│  ├─ Validation Cascade (5 agents)        80K               │
│  ├─ Debug (if needed)                    30K               │
│  ├─ Results Analysis (3 parallel)        20K               │
│  └─ Claude orchestration                  5K               │
│                                                             │
│  Phase 3: Benchmark Refinement                             │
│  ██████████████████████████              ~150K tokens      │
│  │                                                          │
│  ├─ Tech-Doc re-analysis                 20K               │
│  ├─ Refinement execution                 30K               │
│  ├─ Validation cascade (repeat)          80K               │
│  ├─ Results analysis                     15K               │
│  └─ Claude + documentation                5K               │
│                                                             │
│  Phase 4: Advanced Features (Optional)                     │
│  ████████████████████                    ~100K tokens      │
│  │                                                          │
│  ├─ Variance reduction agents            40K               │
│  ├─ Tally builders (parallel)            30K               │
│  ├─ Parallel configurator                20K               │
│  └─ Claude + skills                      10K               │
│                                                             │
│  ═══════════════════════════════════════════════════════   │
│  TOTAL BUDGET:                           ~500K tokens      │
│  ═══════════════════════════════════════════════════════   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

EFFICIENCY STRATEGY:
• Agents: Research, analysis, complex validation (~70% of tokens)
• Skills: Fast execution, building, plotting (~20% of tokens)
• Claude: Orchestration, decisions, gates (~10% of tokens)
```

---

## QUALITY GATE DECISION TREE

```
                        ┌─────────────┐
                        │   START     │
                        │  Workflow   │
                        └─────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     GATE 1        │
                    │ Design Spec       │
                    │   Complete?       │
                    └───────────────────┘
                         │         │
                      YES│         │NO
                         │         ▼
                         │    [Return to
                         │     Phase 1]
                         ▼
                ┌─────────────────┐
                │  Build Model    │
                │   (Phase 2)     │
                └─────────────────┘
                         │
                         ▼
                ┌───────────────────┐
                │     GATE 2        │
                │  All Validators   │
                │      PASS?        │
                └───────────────────┘
                    │         │
                 YES│         │NO
                    │         ▼
                    │    [Debug &
                    │      Fix]
                    │         │
                    │    ┌────┘
                    │    │
                    │◄───┘
                    │
                    ▼
            ┌────────────────┐
            │   RUN MCNP     │
            └────────────────┘
                    │
                    ▼
            ┌───────────────────┐
            │     GATE 3        │
            │  Model Runs?      │
            │  keff Reasonable? │
            │  Converged?       │
            └───────────────────┘
                │         │
             YES│         │NO
                │         ▼
                │    [Fatal Error
                │     Debugger]
                │         │
                │    [Fix & Rerun]
                │         │
                │    ┌────┘
                │    │
                │◄───┘
                │
                ▼
        ┌─────────────────┐
        │ Benchmark       │
        │  Refinement     │
        │  (Phase 3)      │
        └─────────────────┘
                │
                ▼
        ┌───────────────────┐
        │     GATE 4        │
        │ All Refinements   │
        │   Complete?       │
        │ Validators PASS?  │
        └───────────────────┘
            │         │
         YES│         │NO
            │         ▼
            │    [Iterate
            │     Refinements]
            │         │
            │    ┌────┘
            │    │
            │◄───┘
            │
            ▼
    ┌────────────────────┐
    │ BENCHMARK RUN      │
    └────────────────────┘
            │
            ▼
    ┌───────────────────┐
    │     GATE 5        │
    │ keff = Target?    │
    │ C-E = 2.154%?     │
    │ Stats Quality OK? │
    └───────────────────┘
        │         │
     YES│         │NO
        │         ▼
        │    [Investigate
        │     Discrepancy]
        │         │
        │    [Refine More]
        │         │
        │    ┌────┘
        │    │
        │◄───┘
        │
        ▼
┌──────────────────┐
│   VALIDATION     │
│    SUCCESS!      │
└──────────────────┘
```

---

## DATA FLOW DIAGRAM

```
┌────────────────────────────────────────────────────────────────┐
│                      DATA FLOW THROUGH WORKFLOW                │
└────────────────────────────────────────────────────────────────┘

LITERATURE SOURCES
      │
      ├─► msre-benchmark-berkeley.md
      ├─► msre-design-spec.md
      └─► Additional publications
              │
              ▼
    ┌──────────────────────┐
    │ Tech-Doc-Analyzers   │ (3 parallel instances)
    └──────────────────────┘
              │
              ├─► Geometric parameters
              ├─► Material compositions
              ├─► Operating conditions
              └─► Benchmark targets
                        │
                        ▼
              ┌──────────────────┐
              │ CLAUDE           │
              │ Consolidation    │
              └──────────────────┘
                        │
                        ├─► Unified parameter table
                        ├─► Cross-reference matrix
                        └─► Gap analysis
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │ Design Specification Doc │
                    └──────────────────────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  │               │               │
                  ▼               ▼               ▼
        [Geometry Specs]  [Material Specs]  [Physics Specs]
                  │               │               │
                  ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │   Geometry   │ │   Material   │ │   Physics    │
        │   Builders   │ │   Builders   │ │   Builders   │
        └──────────────┘ └──────────────┘ └──────────────┘
                  │               │               │
                  └───────────────┼───────────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │  MCNP Input File │
                        │ (msre_model.inp) │
                        └──────────────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │  Validators      │
                        │  (5-stage)       │
                        └──────────────────┘
                                  │
                          [IF PASS]
                                  │
                                  ▼
                        ┌──────────────────┐
                        │   MCNP6          │
                        │   Execution      │
                        └──────────────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  │               │               │
                  ▼               ▼               ▼
          [Output File]    [MCTAL File]   [Plot Files]
                  │               │               │
                  └───────────────┼───────────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │  Output Parser   │
                        └──────────────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  │               │               │
                  ▼               ▼               ▼
        [keff Results]  [Tally Data]  [Convergence Data]
                  │               │               │
                  └───────────────┼───────────────┘
                                  │
                                  ▼
                        ┌──────────────────────┐
                        │   Analysis Agents    │
                        │   (3 parallel)       │
                        └──────────────────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  │               │               │
                  ▼               ▼               ▼
        [Physics Analysis] [Statistics] [Visualizations]
                  │               │               │
                  └───────────────┼───────────────┘
                                  │
                                  ▼
                        ┌──────────────────────┐
                        │  CLAUDE Synthesis    │
                        └──────────────────────┘
                                  │
                                  ▼
                        ┌──────────────────────┐
                        │  Final Report        │
                        │  • keff vs target    │
                        │  • C-E discrepancy   │
                        │  • Validation status │
                        │  • Plots & tables    │
                        └──────────────────────┘
```

---

## SKILLS vs AGENTS DECISION MATRIX

```
╔════════════════════════════════════════════════════════════════╗
║              WHEN TO USE SKILLS vs AGENTS                      ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  USE SKILLS WHEN:                    USE AGENTS WHEN:         ║
║  ──────────────────                  ─────────────────        ║
║                                                                ║
║  ✓ Task is well-defined              ✓ Need research          ║
║  ✓ Parameters are known              ✓ Need examples          ║
║  ✓ Fast execution needed             ✓ Complex analysis       ║
║  ✓ Simple building/editing           ✓ Multi-step validation  ║
║  ✓ Token efficiency critical         ✓ Debugging required     ║
║  ✓ Direct I/O operation              ✓ Literature extraction  ║
║                                      ✓ Autonomous workflow    ║
║                                                                ║
║  EXAMPLES:                           EXAMPLES:                ║
║  • Plot geometry                     • Analyze benchmark doc  ║
║  • Build material card               • Debug fatal error      ║
║  • Convert units                     • Validate 57 checklist  ║
║  • Edit cell definition              • Find example files     ║
║  • Create simple tally               • Check geometry overlaps║
║                                                                ║
║  TYPICAL TOKEN COST:                 TYPICAL TOKEN COST:      ║
║  2K - 10K per invocation             15K - 50K per invocation ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## COMMUNICATION PROTOCOL DIAGRAM

```
┌───────────────────────────────────────────────────────────────┐
│             HOW TOOLS COMMUNICATE IN WORKFLOW                 │
└───────────────────────────────────────────────────────────────┘

METHOD 1: CLAUDE ORCHESTRATION (Primary)
─────────────────────────────────────────

    Agent A              CLAUDE             Agent B
       │                    │                  │
       │   [Output]         │                  │
       ├───────────────────►│                  │
       │                    │                  │
       │                    │ [Review]         │
       │                    │ [Analyze]        │
       │                    │ [Prepare         │
       │                    │  context]        │
       │                    │                  │
       │                    │ [Instructions]   │
       │                    ├─────────────────►│
       │                    │                  │
       │                    │      [Output]    │
       │                    │◄─────────────────┤
       │                    │                  │


METHOD 2: SHARED FILES (Secondary)
───────────────────────────────────

    Agent A                            Agent B
       │                                  │
       │  [Write results to              │
       │   validation_report.md]         │
       ├──────────────────►               │
       │                  │               │
       │                  │               │
       │                  │  [Read        │
       │                  │   validation_ │
       │                  │   report.md]  │
       │                  └──────────────►│
       │                                  │


METHOD 3: CLAUDE MEDIATES SKILL-AGENT
──────────────────────────────────────

    Skill              CLAUDE             Agent
      │                  │                 │
      │  [Fast build]    │                 │
      ├─────────────────►│                 │
      │                  │                 │
      │                  │ [Quick review]  │
      │                  │ [Add context]   │
      │                  │                 │
      │                  │ [Deep validate] │
      │                  ├────────────────►│
      │                  │                 │
      │                  │   [Report]      │
      │                  │◄────────────────┤
      │                  │                 │
      │                  │ [Decision]      │
      │                  │                 │
```

---

**END OF WORKFLOW DIAGRAMS**

Use these visualizations alongside the detailed MSRE_WORKFLOW_VALIDATION_PLAN.md
for comprehensive understanding of the integration testing approach.

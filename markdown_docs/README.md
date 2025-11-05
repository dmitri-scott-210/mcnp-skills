# MCNP6.3.1 Documentation - Markdown Edition

This directory contains the complete MCNP6.3.1 documentation converted from PDF to Markdown format using Docling MCP Server. The documentation has been organized into logical sections with metadata front matter for easy navigation and reference.

## Conversion Information

- **Conversion Date**: 2025-10-30
- **Conversion Tool**: Docling MCP Server + Claude
- **Source Version**: MCNP6.3.1 Official Documentation
- **Total Documents**: 71 markdown files
- **Format**: CommonMark-compliant Markdown with YAML front matter

## Directory Structure

```
markdown_docs/
├── theory_manual/         # MCNP Theory Manual (13 chapters)
├── user_manual/           # MCNP User Manual (21 chapters)
├── examples/              # Practical Examples (6 chapters)
├── primers/               # MCNP Primers (6 documents)
├── appendices/            # Technical Appendices (25 documents)
└── images/                # Placeholder for extracted images
```

---

## Table of Contents

### 1. Theory Manual (13 Documents)

The Theory Manual provides the mathematical and physical foundations of MCNP.

| Chapter | Title | File |
|---------|-------|------|
| 1 | MCNP Code Overview | [01_MCNP_Code_Overview.md](theory_manual/01_MCNP_Code_Overview.md) |
| 2.1 | Introduction | [chapter_02/02_01_Introduction.md](theory_manual/chapter_02/02_01_Introduction.md) |
| 2.2 | Geometry | [chapter_02/02_02_Geometry.md](theory_manual/chapter_02/02_02_Geometry.md) |
| 2.3 | Cross Sections | [chapter_02/02_03_Cross_Sections.md](theory_manual/chapter_02/02_03_Cross_Sections.md) |
| 2.4 | Physics | [chapter_02/02_04_Physics.md](theory_manual/chapter_02/02_04_Physics.md) |
| 2.5 | Tallies | [chapter_02/02_05_Tallies.md](theory_manual/chapter_02/02_05_Tallies.md) |
| 2.6 | Estimation of the Monte Carlo Precision | [chapter_02/02_06_Estimation_of_MC_Precision.md](theory_manual/chapter_02/02_06_Estimation_of_MC_Precision.md) |
| 2.7 | Variance Reduction | [chapter_02/02_07_Variance_Reduction.md](theory_manual/chapter_02/02_07_Variance_Reduction.md) |
| 2.8 | Criticality Calculations | [chapter_02/02_08_Criticality_Calculations.md](theory_manual/chapter_02/02_08_Criticality_Calculations.md) |
| 2.9 | Volumes and Areas | [chapter_02/02_09_Volumes_and_Areas.md](theory_manual/chapter_02/02_09_Volumes_and_Areas.md) |
| 2.10 | Plotter | [chapter_02/02_10_Plotter.md](theory_manual/chapter_02/02_10_Plotter.md) |
| 2.11 | Random Numbers | [chapter_02/02_11_Random_Numbers.md](theory_manual/chapter_02/02_11_Random_Numbers.md) |
| 2.12 | Perturbations | [chapter_02/02_12_Perturbations.md](theory_manual/chapter_02/02_12_Perturbations.md) |

---

### 2. User Manual (21 Documents)

The User Manual provides comprehensive guidance on creating and running MCNP simulations.

#### General Introduction

| Chapter | Title | File |
|---------|-------|------|
| 3 | Introduction to MCNP Usage | [03_Introduction_to_MCNP_Usage.md](user_manual/03_Introduction_to_MCNP_Usage.md) |
| 4 | Description of MCNP6 Input | [04_Description_of_MCNP6_Input.md](user_manual/04_Description_of_MCNP6_Input.md) |

#### Chapter 5: Input Cards (13 Documents)

Complete reference for all MCNP input card types.

| Section | Title | File |
|---------|-------|------|
| 5.1 | Geometry Specification Card Introduction | [chapter_05_input_cards/05_01_Geometry_Specification_Intro.md](user_manual/chapter_05_input_cards/05_01_Geometry_Specification_Intro.md) |
| 5.2 | Cell Cards | [chapter_05_input_cards/05_02_Cell_Cards.md](user_manual/chapter_05_input_cards/05_02_Cell_Cards.md) |
| 5.3 | Surface Cards | [chapter_05_input_cards/05_03_Surface_Cards.md](user_manual/chapter_05_input_cards/05_03_Surface_Cards.md) |
| 5.4 | Data Card Introduction | **MISSING** - PDF conversion failed |
| 5.5 | Geometry-focused Data Cards | [chapter_05_input_cards/05_05_Geometry_Data_Cards.md](user_manual/chapter_05_input_cards/05_05_Geometry_Data_Cards.md) |
| 5.6 | Material-focused Data Cards | [chapter_05_input_cards/05_06_Material_Data_Cards.md](user_manual/chapter_05_input_cards/05_06_Material_Data_Cards.md) |
| 5.7 | Physics-focused Data Cards | [chapter_05_input_cards/05_07_Physics_Data_Cards.md](user_manual/chapter_05_input_cards/05_07_Physics_Data_Cards.md) |
| 5.8 | Source Specification-focused Data Cards | [chapter_05_input_cards/05_08_Source_Data_Cards.md](user_manual/chapter_05_input_cards/05_08_Source_Data_Cards.md) |
| 5.9 | Tally Specification-focused Data Cards | [chapter_05_input_cards/05_09_Tally_Data_Cards.md](user_manual/chapter_05_input_cards/05_09_Tally_Data_Cards.md) |
| 5.10 | Tally Perturbations and Reactivity Sensitivity | [chapter_05_input_cards/05_10_Tally_Perturbations.md](user_manual/chapter_05_input_cards/05_10_Tally_Perturbations.md) |
| 5.11 | Superimposed Mesh Tallies | [chapter_05_input_cards/05_11_Mesh_Tallies.md](user_manual/chapter_05_input_cards/05_11_Mesh_Tallies.md) |
| 5.12 | Variance Reduction-focused Data Cards | [chapter_05_input_cards/05_12_Variance_Reduction_Cards.md](user_manual/chapter_05_input_cards/05_12_Variance_Reduction_Cards.md) |
| 5.13 | Problem Termination, Output Control, and Misc | [chapter_05_input_cards/05_13_Output_Control_Misc.md](user_manual/chapter_05_input_cards/05_13_Output_Control_Misc.md) |

#### Chapter 6: Plotting and Visualization (5 Documents)

| Section | Title | File |
|---------|-------|------|
| 6.1 | System Graphics Information | [chapter_06_plotting/06_01_System_Graphics.md](user_manual/chapter_06_plotting/06_01_System_Graphics.md) |
| 6.2 | The Geometry Plotter, PLOT | [chapter_06_plotting/06_02_Geometry_Plotter.md](user_manual/chapter_06_plotting/06_02_Geometry_Plotter.md) |
| 6.3 | The Tally and Cross-Section Plotter, MCPLOT | [chapter_06_plotting/06_03_Tally_Plotter.md](user_manual/chapter_06_plotting/06_03_Tally_Plotter.md) |
| 6.4 | Tally Plotting Examples | [chapter_06_plotting/06_04_Tally_Plot_Examples.md](user_manual/chapter_06_plotting/06_04_Tally_Plot_Examples.md) |
| 6.5 | Normalization of Energy-dependent Tally Plots | [chapter_06_plotting/06_05_Tally_Normalization.md](user_manual/chapter_06_plotting/06_05_Tally_Normalization.md) |

#### Advanced Topics (2 Documents)

| Chapter | Title | File |
|---------|-------|------|
| 7 | Technology Preview Qt Based MCNP Geometry and Tally Viewer | [07_Qt_Preview.md](user_manual/07_Qt_Preview.md) |
| 8 | Unstructured Mesh | [08_Unstructured_Mesh.md](user_manual/08_Unstructured_Mesh.md) |

---

### 3. Examples (6 Documents)

Practical examples demonstrating MCNP capabilities.

| Chapter | Title | File |
|---------|-------|------|
| 9 | Introduction | [09_Introduction.md](examples/09_Introduction.md) |
| 10.1 | Geometry Examples | [chapter_10/10_01_Geometry_Examples.md](examples/chapter_10/10_01_Geometry_Examples.md) |
| 10.2 | Tally Examples | [chapter_10/10_02_Tally_Examples.md](examples/chapter_10/10_02_Tally_Examples.md) |
| 10.3 | Source Examples | [chapter_10/10_03_Source_Examples.md](examples/chapter_10/10_03_Source_Examples.md) |
| 10.4 | Material Examples | **MISSING** - PDF conversion failed |
| 10.5 | Physics Models | [chapter_10/10_05_Physics_Models.md](examples/chapter_10/10_05_Physics_Models.md) |
| 10.6 | Variance Reduction Examples | [chapter_10/10_06_Variance_Reduction_Examples.md](examples/chapter_10/10_06_Variance_Reduction_Examples.md) |

---

### 4. Primers (6 Documents)

Beginner-friendly guides to MCNP concepts.

| Document | Title | File |
|----------|-------|------|
| - | MCNP6 Primer | [MCNP6_Primer.md](primers/MCNP6_Primer.md) |

#### Source Primer Series

| Chapter | Title | File |
|---------|-------|------|
| 1 | What is this document | [source_primer/01_What_is_this_document.md](primers/source_primer/01_What_is_this_document.md) |
| 2 | Basic Sources | [source_primer/02_Basic_Sources.md](primers/source_primer/02_Basic_Sources.md) |
| 3 | Intermediate Sources | [source_primer/03_Intermediate_Sources.md](primers/source_primer/03_Intermediate_Sources.md) |
| 4 | Advanced Sources | [source_primer/04_Advanced_Sources.md](primers/source_primer/04_Advanced_Sources.md) |
| 5 | Known Source Errors | [source_primer/05_Known_Source_Errors.md](primers/source_primer/05_Known_Source_Errors.md) |

---

### 5. Appendices (25 Documents)

Technical references and utility documentation.

#### Appendix A-C: File Formats

| Appendix | Title | File |
|----------|-------|------|
| A | Mesh-Based WWINP, WWOUT, and WWONE File Format | [AppendixA_Mesh_File_Formats.md](appendices/AppendixA_Mesh_File_Formats.md) |
| B | XSDIR Data Directory File | [AppendixB_XSDIR.md](appendices/AppendixB_XSDIR.md) |
| C | Transportable Heavy Ions | [AppendixC_Heavy_Ions.md](appendices/AppendixC_Heavy_Ions.md) |

#### Appendix D: Data File Formats (9 Documents)

| Section | Title | File |
|---------|-------|------|
| D.1 | Overview of HDF5 in the MCNP Code | **MISSING** - PDF conversion failed |
| D.2 | Restart File Format | [AppendixD_02_Restart_File_Format.md](appendices/AppendixD_02_Restart_File_Format.md) |
| D.3 | Particle Track Output File Format | [AppendixD_03_Particle_Track_Output.md](appendices/AppendixD_03_Particle_Track_Output.md) |
| D.4 | Mesh Tally XDMF Output Format | [AppendixD_04_Mesh_Tally_XDMF.md](appendices/AppendixD_04_Mesh_Tally_XDMF.md) |
| D.5 | Fission Matrix Format | [AppendixD_05_Fission_Matrix.md](appendices/AppendixD_05_Fission_Matrix.md) |
| D.6 | Unstructured Mesh File Format HDF5 | [AppendixD_06_Unstructured_Mesh_HDF5.md](appendices/AppendixD_06_Unstructured_Mesh_HDF5.md) |
| D.7 | Unstructured Mesh File Format Legacy EEOUT | [AppendixD_07_Unstructured_Mesh_Legacy.md](appendices/AppendixD_07_Unstructured_Mesh_Legacy.md) |
| D.8 | Script to Generate HDF5 File Layouts | [AppendixD_08_HDF5_Script.md](appendices/AppendixD_08_HDF5_Script.md) |
| D.9 | inxc File Structure | [AppendixD_09_inxc_File_Structure.md](appendices/AppendixD_09_inxc_File_Structure.md) |

#### Appendix E: Utility Tools (12 Documents)

| Section | Title | File |
|---------|-------|------|
| E.1 | Doppler Broadening Resonance Correction Library | [AppendixE_01_Doppler_Broadening.md](appendices/AppendixE_01_Doppler_Broadening.md) |
| E.2 | Event Log Analyzer (ela.pl) | [AppendixE_02_Event_Log_Analyzer.md](appendices/AppendixE_02_Event_Log_Analyzer.md) |
| E.3 | On-the-fly Doppler Broadened Data Fitting | [AppendixE_03_Doppler_Fitting.md](appendices/AppendixE_03_Doppler_Fitting.md) |
| E.4 | Gridconv (gridconv) | [AppendixE_04_Gridconv.md](appendices/AppendixE_04_Gridconv.md) |
| E.5 | Cross Section Library Manipulation Tool (makxsf) | [AppendixE_05_Cross_Section_Tool.md](appendices/AppendixE_05_Cross_Section_Tool.md) |
| E.6 | Merge ASCII Tally Files (merge_mctal.pl) | [AppendixE_06_Merge_ASCII_Tally.md](appendices/AppendixE_06_Merge_ASCII_Tally.md) |
| E.7 | Merge Mesh Tally Files (merge_meshtal.pl) | [AppendixE_07_Merge_Mesh_Tally.md](appendices/AppendixE_07_Merge_Mesh_Tally.md) |
| E.8 | Parameter Study and Uncertainty Analysis Tool | [AppendixE_08_Parameter_Study_Tool.md](appendices/AppendixE_08_Parameter_Study_Tool.md) |
| E.9 | Simple ACE File Generation Tools (simple_ace.pl) | [AppendixE_09_Simple_ACE_Tools.md](appendices/AppendixE_09_Simple_ACE_Tools.md) |
| E.10 | Unstructured Mesh Format Converter (um_converter) | [AppendixE_10_UM_Converter.md](appendices/AppendixE_10_UM_Converter.md) |
| E.11 | Unstructured Mesh Post-processing (um_post_op) | [AppendixE_11_UM_Post_Processing.md](appendices/AppendixE_11_UM_Post_Processing.md) |
| E.12 | Unstructured Mesh Pre-processing (um_pre_op) | [AppendixE_12_UM_Pre_Processing.md](appendices/AppendixE_12_UM_Pre_Processing.md) |

#### Appendix F: Conversion Factors (2 Documents)

| Section | Title | File |
|---------|-------|------|
| F.1 | Biological Conversion Factors | [AppendixF_01_Biological_Conversion.md](appendices/AppendixF_01_Biological_Conversion.md) |
| F.2 | Silicon Displacement Factors | [AppendixF_02_Silicon_Displacement.md](appendices/AppendixF_02_Silicon_Displacement.md) |

---

## Quick Reference by Topic

### Getting Started
- [Introduction to MCNP Usage](user_manual/03_Introduction_to_MCNP_Usage.md)
- [MCNP6 Primer](primers/MCNP6_Primer.md)
- [MCNP Code Overview](theory_manual/01_MCNP_Code_Overview.md)

### Geometry Modeling
- [Geometry Theory](theory_manual/chapter_02/02_02_Geometry.md)
- [Cell Cards](user_manual/chapter_05_input_cards/05_02_Cell_Cards.md)
- [Surface Cards](user_manual/chapter_05_input_cards/05_03_Surface_Cards.md)
- [Geometry Examples](examples/chapter_10/10_01_Geometry_Examples.md)
- [Geometry Plotter](user_manual/chapter_06_plotting/06_02_Geometry_Plotter.md)

### Materials and Physics
- [Material-focused Data Cards](user_manual/chapter_05_input_cards/05_06_Material_Data_Cards.md)
- [Physics-focused Data Cards](user_manual/chapter_05_input_cards/05_07_Physics_Data_Cards.md)
- [Cross Sections](theory_manual/chapter_02/02_03_Cross_Sections.md)
- [Physics Theory](theory_manual/chapter_02/02_04_Physics.md)

### Source Definitions
- [Source Specification Cards](user_manual/chapter_05_input_cards/05_08_Source_Data_Cards.md)
- [Source Examples](examples/chapter_10/10_03_Source_Examples.md)
- [Source Primer Series](primers/source_primer/)

### Tallies and Output
- [Tally Theory](theory_manual/chapter_02/02_05_Tallies.md)
- [Tally Specification Cards](user_manual/chapter_05_input_cards/05_09_Tally_Data_Cards.md)
- [Mesh Tallies](user_manual/chapter_05_input_cards/05_11_Mesh_Tallies.md)
- [Tally Examples](examples/chapter_10/10_02_Tally_Examples.md)
- [Tally Plotting](user_manual/chapter_06_plotting/06_03_Tally_Plotter.md)

### Variance Reduction
- [Variance Reduction Theory](theory_manual/chapter_02/02_07_Variance_Reduction.md)
- [Variance Reduction Cards](user_manual/chapter_05_input_cards/05_12_Variance_Reduction_Cards.md)
- [Variance Reduction Examples](examples/chapter_10/10_06_Variance_Reduction_Examples.md)
- [Weight Window Files](appendices/AppendixA_Mesh_File_Formats.md)

### Criticality Calculations
- [Criticality Theory](theory_manual/chapter_02/02_08_Criticality_Calculations.md)
- [KCODE Card](user_manual/chapter_05_input_cards/05_08_Source_Data_Cards.md)

### Advanced Features
- [Unstructured Mesh](user_manual/08_Unstructured_Mesh.md)
- [Unstructured Mesh Tools](appendices/AppendixE_10_UM_Converter.md)
- [Tally Perturbations](user_manual/chapter_05_input_cards/05_10_Tally_Perturbations.md)

### Utilities and Tools
- [Event Log Analyzer](appendices/AppendixE_02_Event_Log_Analyzer.md)
- [Parameter Study Tool](appendices/AppendixE_08_Parameter_Study_Tool.md)
- [Cross Section Tools](appendices/AppendixE_05_Cross_Section_Tool.md)

---

## Known Issues

### Missing Documents (3 PDFs Failed Conversion)

The following PDFs could not be converted due to file corruption in the source:

1. **5.4_Data_Card_Introduction.pdf** - Data card overview chapter
2. **10.4_Material_Examples.pdf** - Material specification examples
3. **D.1_Overview_of_HDF5_in_the_MCNP_Code.pdf** - HDF5 format introduction

**Note**: These documents should be obtained from official MCNP distribution sources and re-converted separately.

### Conversion Limitations

- **Equations**: Mathematical equations appear as `<!-- formula-not-decoded -->` placeholders
- **Images**: Images are marked with `<!-- image -->` placeholders
- **Tables**: Complex tables may have formatting issues
- **Code Blocks**: MCNP input examples should be manually verified

---

## Usage Recommendations

### For Learning MCNP
1. Start with [MCNP6 Primer](primers/MCNP6_Primer.md)
2. Read [Introduction to MCNP Usage](user_manual/03_Introduction_to_MCNP_Usage.md)
3. Study [Geometry Examples](examples/chapter_10/10_01_Geometry_Examples.md)
4. Explore [Source Primer](primers/source_primer/02_Basic_Sources.md)

### For Reference
- Use Chapter 5 sections for card syntax reference
- Consult Theory Manual for physics/mathematical details
- Check Appendices for file formats and utility tools

### For Troubleshooting
- Review [Known Source Errors](primers/source_primer/05_Known_Source_Errors.md)
- Check input card syntax in Chapter 5
- Verify geometry with plotter tools (Chapter 6)

---

## Additional Resources

### External Links
- [Official MCNP Website](https://mcnp.lanl.gov/)
- [RSICC Code Package](https://rsicc.ornl.gov/codes/ccc/ccc8/ccc-870.html)
- [MCNP Forum](https://mcnp.lanl.gov/forum.html)

### Training Materials
- MCNP6 Primer by J. Kenneth Shultis (included in primers/)
- Visual Editor documentation
- LANL training courses

---

## License and Copyright

This documentation is derived from official MCNP6.3.1 materials developed by Los Alamos National Laboratory. MCNP® is a registered trademark of Los Alamos National Security, LLC, which manages and operates Los Alamos National Laboratory under contract with the U.S. Department of Energy.

**Conversion performed for educational and reference purposes only.**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-30 | Initial conversion of 71/75 documents from MCNP6.3.1 official PDFs |

---

## Contact and Contributions

For issues with the markdown conversion or formatting, please refer to the PROJECT_HANDOFF.md file in the parent directory.

For MCNP technical questions, consult the official MCNP documentation or contact RSICC.

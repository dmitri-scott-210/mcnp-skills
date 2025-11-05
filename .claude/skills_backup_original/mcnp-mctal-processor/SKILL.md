---
name: "MCNP MCTAL Processor"
description: "Processes MCTAL tally files for export, conversion, merging, and custom analysis. Extracts machine-readable tally data. Use when working with MCTAL files."
version: "1.0.0"
dependencies: "python>=3.8, numpy, pandas"
---

# MCNP MCTAL Processor

## Overview

When a user needs to work with MCTAL (Machine-readable tally) files, use this skill to:

- **Parse MCTAL files**: Extract tally data, headers, metadata
- **Export to formats**: CSV, Excel, JSON, HDF5 for external analysis
- **Merge MCTAL files**: Combine results from multiple runs (parameter studies, parallel jobs)
- **Convert formats**: MCTAL → other formats for plotting tools
- **Extract specific data**: Individual tallies, energy bins, specific segments
- **Validate MCTAL integrity**: Check file completeness, verify data consistency

MCTAL files are MCNP's machine-readable tally output format, designed for programmatic access rather than human reading. They contain all tally information in a structured ASCII format that's easier to parse than the main OUTP file.

## Workflow Decision Tree

### When to Invoke This Skill

**Autonomous Invocation Triggers:**
- User mentions "MCTAL", "mctal file", or "machine-readable tally"
- User wants to "export tally data" or "extract tally results"
- User needs to "merge runs", "combine tallies", or "average results"
- User wants data in Excel, CSV, or other analysis-friendly format
- User mentions MCPLOT or asks about tally file format
- User has multiple runs to combine (parameter study, parallel execution)
- User wants to process tally data with external tools (MATLAB, Python, R)

**Context Clues:**
- "Export tallies to spreadsheet..."
- "Combine results from my parameter study..."
- "Get tally data into Python..."
- "Merge parallel MCNP runs..."
- "Convert MCTAL to CSV..."

### Processing Type Decision Tree

**Step 1: Determine Operation**

```
User request → Select processing type:
├── Parse single file → Extract data from one MCTAL
├── Export/convert → Save in different format
├── Merge files → Combine multiple MCALs
├── Extract subset → Get specific tallies/bins
├── Validate file → Check integrity
└── Custom processing → User-defined operations
```

**Step 2: Select Output Format**

```
Export format needed:
├── CSV → Tabular data for Excel/spreadsheets
├── Excel → Multi-sheet workbook with metadata
├── JSON → Structured data for web applications
├── HDF5 → Large datasets, hierarchical structure
├── Pandas DataFrame → Python data analysis
└── NumPy arrays → Numerical computing
```

**Step 3: Processing Complexity**

```
Simple extraction:
├── Single tally from single file
├── Direct format conversion
└── Standard export

Moderate processing:
├── Multiple tallies extracted
├── Specific binning selections
├── Merge 2-5 files
└── Custom column arrangement

Complex processing:
├── Merge many files (>5)
├── Weighted averages
├── Statistical combinations
├── Custom data transformations
└── Batch processing
```

## Tool Invocation

This skill includes a Python implementation for automated MCTAL file processing and extraction.

### Importing the Tool

```python
from mcnp_mctal_parser import MCNPMCTALParser

# Initialize the parser
parser = MCNPMCTALParser()
```

### Basic Usage

**Parse Complete MCTAL File**:
```python
# Parse entire MCTAL file
data = parser.parse_mctal('mctal')

# Access header information
header = data['header']
print(f"NPS: {header['nps']}")
print(f"Problem ID: {header['probid']}")

# Access all tallies
tallies = data['tallies']
print(f"Number of tallies: {len(tallies)}")
```

**List All Tallies in File**:
```python
# Get list of tally numbers
tally_numbers = parser.list_tallies('mctal')

print("Tallies in file:")
for tally_num in tally_numbers:
    print(f"  F{tally_num}")
```

**Extract Specific Tally**:
```python
# Extract single tally data
tally_4 = parser.extract_tally('mctal', tally_num=4)

if tally_4:
    print(f"Tally F4:")
    print(f"  Values: {tally_4['values']}")
    print(f"  Errors: {tally_4['errors']}")
    print(f"  Energy bins: {tally_4['energy_bins']}")
else:
    print("Tally 4 not found in MCTAL file")
```

**Export to JSON**:
```python
# Convert MCTAL to JSON format
parser.export_to_json('mctal', 'tally_data.json')
print("MCTAL data exported to tally_data.json")

# Can now process with any JSON-capable tool
```

### Integration with MCNP Workflow

```python
from mcnp_mctal_parser import MCNPMCTALParser
import json

def extract_and_analyze_tallies(mctal_file, output_csv='tally_results.csv'):
    """Extract tally data and export for analysis"""
    print(f"Processing MCTAL file: {mctal_file}")
    print("=" * 60)

    parser = MCNPMCTALParser()

    # Parse MCTAL file
    data = parser.parse_mctal(mctal_file)

    # Display header information
    header = data['header']
    print(f"\n📋 SIMULATION INFO:")
    print(f"  Problem ID: {header.get('probid', 'N/A')}")
    print(f"  Histories: {header.get('nps', 0):,}")
    print(f"  Random seed: {header.get('random_seed', 'N/A')}")

    # List all tallies
    tallies = data['tallies']
    print(f"\n📊 TALLIES FOUND:")
    print(f"  Total tallies: {len(tallies)}")

    for tally_num in sorted(tallies.keys()):
        tally = tallies[tally_num]
        tally_type = f"F{tally_num}"

        # Determine tally type
        if tally_num % 10 == 1:
            ttype = "Surface Current"
        elif tally_num % 10 == 2:
            ttype = "Surface Flux"
        elif tally_num % 10 == 4:
            ttype = "Cell Flux"
        elif tally_num % 10 == 5:
            ttype = "Point Detector"
        elif tally_num % 10 == 6:
            ttype = "Energy Deposition"
        elif tally_num % 10 == 7:
            ttype = "Fission Energy Deposition"
        elif tally_num % 10 == 8:
            ttype = "Pulse Height"
        else:
            ttype = "Other"

        print(f"  {tally_type}: {ttype}")

        # Show basic statistics
        if 'values' in tally and 'errors' in tally:
            values = tally['values']
            errors = tally['errors']
            if values:
                total_val = sum(values)
                avg_error = sum(errors) / len(errors) if errors else 0
                print(f"    Total: {total_val:.4e}, Avg Error: {avg_error:.4f}")

    # Export to JSON for external analysis
    json_file = mctal_file + '.json'
    parser.export_to_json(mctal_file, json_file)
    print(f"\n💾 Data exported to: {json_file}")

    # Export to CSV (if simple structure)
    try:
        import pandas as pd

        # Create simple CSV with summary data
        rows = []
        for tally_num, tally in tallies.items():
            if 'values' in tally and 'errors' in tally:
                for i, (val, err) in enumerate(zip(tally['values'], tally['errors'])):
                    rows.append({
                        'Tally': f"F{tally_num}",
                        'Bin': i + 1,
                        'Value': val,
                        'RelError': err
                    })

        if rows:
            df = pd.DataFrame(rows)
            df.to_csv(output_csv, index=False)
            print(f"💾 CSV summary exported to: {output_csv}")

    except ImportError:
        print("  (pandas not available - skipping CSV export)")

    print("\n" + "=" * 60)
    print("✓ MCTAL processing complete")

    return data

# Example usage
if __name__ == "__main__":
    import sys

    mctal_file = sys.argv[1] if len(sys.argv) > 1 else "mctal"

    # Process MCTAL file
    data = extract_and_analyze_tallies(mctal_file)

    # Example: Access specific tally for further analysis
    parser = MCNPMCTALParser()
    tally_4 = parser.extract_tally(mctal_file, 4)

    if tally_4:
        print("\n📈 DETAILED TALLY 4 ANALYSIS:")
        print(f"  Number of bins: {len(tally_4.get('values', []))}")

        # Show energy bins if available
        if 'energy_bins' in tally_4:
            print(f"  Energy bins: {len(tally_4['energy_bins'])}")
            for i, (elow, ehigh) in enumerate(zip(tally_4['energy_bins'][:-1],
                                                   tally_4['energy_bins'][1:])):
                if i < len(tally_4['values']):
                    val = tally_4['values'][i]
                    err = tally_4['errors'][i]
                    print(f"    Bin {i+1}: {elow:.2e} - {ehigh:.2e} MeV")
                    print(f"            Value: {val:.4e} ± {err:.1%}")
```

---

## MCTAL File Format

### Structure (from MCNP documentation)

**Line 1: Header**
```
kod    ver    probid
```
- `kod`: Code identifier
- `ver`: MCNP version
- `probid`: Problem identification string

**Line 2: Counts**
```
knod   ntal   jtty   npert   (comment line)
```
- `ntal`: Number of tallies in file
- `npert`: Number of perturbations

**Line 3: NPS and Random**
```
nps    rnr
```
- `nps`: Number of particle histories run
- `rnr`: Random number seed

**Tally Block (repeated for each tally):**
```
f   d   u   s   m   c   e   t   (tally descriptor)
```
- `f`: Tally number
- `d`: Detector flag (0=no, 1=point detector, 2=ring detector)
- `u`: User bin flag
- `s`: Segment flag
- `m`: Multiplier flag (FM card)
- `c`: Cosine bin flag
- `e`: Energy bin flag
- `t`: Time bin flag

**Binning Data:**
For each flagged dimension:
```
n_bins
bin_1 bin_2 ... bin_n
```

**Tally Values:**
```
value_1  error_1
value_2  error_2
...
value_n  error_n
```

**TFC Data (optional):**
```
tfc  jtf
nps_1  mean_1  error_1  vov_1  slope_1  fom_1
nps_2  mean_2  error_2  vov_2  slope_2  fom_2
...
```

### Example MCTAL File:
```
mcnp     6.3       04/15/24 14:23:15     probid = reactor_model
     2     2     1     0  ntal npert
   1000000  123456789  nps rnr
      4  0  0  0  0  0  1  0        $ F4 tally, energy bins only
     1  10                          $ Cell 10
     5                              $ 5 energy bins
  0.000E+00  1.000E-06  1.000E-03  1.000E-01  1.000E+00  1.400E+01
 1.234E-04  0.0521                 $ Bin 1: thermal
 5.678E-05  0.0789                 $ Bin 2: epithermal
 3.456E-05  0.0912                 $ Bin 3: intermediate
 1.234E-05  0.1234                 $ Bin 4: fast
 8.901E-06  0.1567                 $ Bin 5: source energy
 2.734E-04  0.0321                 $ Total
tfc     8
   100000  2.65E-04  0.0987  0.156  2.1  1.3E+02  0  0
   250000  2.71E-04  0.0654  0.078  2.5  1.3E+02  0  0
   500000  2.70E-04  0.0432  0.043  2.8  1.4E+02  0  0
  1000000  2.70E-04  0.0321  0.025  2.9  1.3E+02  0  0
```

## Processing Procedures

### Step 1: Initial Assessment

**Ask user for context:**
- "What MCTAL file(s) do you need to process?" (file paths)
- "What do you want to do?" (parse, export, merge, extract)
- "What format do you need?" (CSV, Excel, JSON, DataFrame)
- "Which tallies?" (specific numbers or all)
- "Any specific binning?" (energy bins, time bins, all bins)

### Step 2: Read Reference Materials

**MANDATORY - READ ENTIRE FILE**: Before processing, read:
- `.claude/commands/mcnp-mctal-processor.md` - Complete processing procedures
- If needed: Review MCTAL format in knowledge base

### Step 3: Parse MCTAL File

**Python parsing implementation:**

```python
import re
import numpy as np

class MCTALProcessor:
    """Process MCNP MCTAL files"""

    def __init__(self):
        self.header = {}
        self.tallies = {}

    def parse_file(self, filepath):
        """Parse MCTAL file completely"""

        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Parse header (lines 1-3)
        header_line = lines[0].strip().split()
        self.header['code'] = header_line[0]
        self.header['version'] = header_line[1]
        self.header['probid'] = ' '.join(header_line[2:])

        # Parse counts
        counts_line = lines[1].strip().split()
        n_tallies = int(counts_line[1])
        n_pert = int(counts_line[3])

        # Parse NPS and random seed
        nps_line = lines[2].strip().split()
        self.header['nps'] = int(nps_line[0])
        self.header['random_seed'] = int(nps_line[1])

        # Parse tallies
        line_idx = 3
        for i_tally in range(n_tallies):
            tally, line_idx = self._parse_tally(lines, line_idx)
            self.tallies[tally['number']] = tally

        return {
            'header': self.header,
            'tallies': self.tallies
        }

    def _parse_tally(self, lines, start_idx):
        """Parse individual tally block"""

        # Tally descriptor line
        desc = lines[start_idx].strip().split()
        tally = {
            'number': int(desc[0]),
            'detector_flag': int(desc[1]),
            'user_flag': int(desc[2]),
            'segment_flag': int(desc[3]),
            'multiplier_flag': int(desc[4]),
            'cosine_flag': int(desc[5]),
            'energy_flag': int(desc[6]),
            'time_flag': int(desc[7])
        }
        line_idx = start_idx + 1

        # Parse cell/surface list
        n_cells = int(lines[line_idx].strip())
        line_idx += 1
        tally['cells'] = []
        while len(tally['cells']) < n_cells:
            cells = [int(x) for x in lines[line_idx].strip().split()]
            tally['cells'].extend(cells)
            line_idx += 1

        # Parse energy bins (if flagged)
        if tally['energy_flag']:
            n_ebins = int(lines[line_idx].strip())
            line_idx += 1
            tally['energy_bins'] = []
            while len(tally['energy_bins']) < n_ebins + 1:  # +1 for boundaries
                ebins = [float(x) for x in lines[line_idx].strip().split()]
                tally['energy_bins'].extend(ebins)
                line_idx += 1
            tally['n_energy_bins'] = n_ebins
        else:
            tally['n_energy_bins'] = 1
            tally['energy_bins'] = [0.0, float('inf')]

        # Parse time bins (if flagged)
        if tally['time_flag']:
            n_tbins = int(lines[line_idx].strip())
            line_idx += 1
            tally['time_bins'] = []
            while len(tally['time_bins']) < n_tbins + 1:
                tbins = [float(x) for x in lines[line_idx].strip().split()]
                tally['time_bins'].extend(tbins)
                line_idx += 1
            tally['n_time_bins'] = n_tbins
        else:
            tally['n_time_bins'] = 1
            tally['time_bins'] = [0.0, float('inf')]

        # Parse cosine bins (if flagged)
        if tally['cosine_flag']:
            n_cbins = int(lines[line_idx].strip())
            line_idx += 1
            tally['cosine_bins'] = []
            while len(tally['cosine_bins']) < n_cbins + 1:
                cbins = [float(x) for x in lines[line_idx].strip().split()]
                tally['cosine_bins'].extend(cbins)
                line_idx += 1
            tally['n_cosine_bins'] = n_cbins
        else:
            tally['n_cosine_bins'] = 1

        # Calculate total number of bins
        n_total_bins = (tally['n_energy_bins'] * tally['n_time_bins'] *
                        tally['n_cosine_bins'] * len(tally['cells']))
        n_total_bins += 1  # +1 for total

        # Parse values and errors
        tally['values'] = []
        tally['errors'] = []

        while len(tally['values']) < n_total_bins:
            data_line = lines[line_idx].strip().split()
            if len(data_line) >= 2:
                tally['values'].append(float(data_line[0]))
                tally['errors'].append(float(data_line[1]))
            line_idx += 1

        # Parse TFC data (if present)
        if line_idx < len(lines) and 'tfc' in lines[line_idx].lower():
            tfc_header = lines[line_idx].strip().split()
            n_tfc_lines = int(tfc_header[1])
            line_idx += 1

            tally['tfc'] = {
                'nps': [],
                'mean': [],
                'error': [],
                'vov': [],
                'slope': [],
                'fom': []
            }

            for i in range(n_tfc_lines):
                tfc_data = lines[line_idx].strip().split()
                tally['tfc']['nps'].append(int(tfc_data[0]))
                tally['tfc']['mean'].append(float(tfc_data[1]))
                tally['tfc']['error'].append(float(tfc_data[2]))
                tally['tfc']['vov'].append(float(tfc_data[3]))
                tally['tfc']['slope'].append(float(tfc_data[4]))
                tally['tfc']['fom'].append(float(tfc_data[5]))
                line_idx += 1

        return tally, line_idx

    def get_tally(self, tally_number):
        """Extract specific tally"""
        return self.tallies.get(tally_number)

    def export_to_csv(self, tally_number, output_file):
        """Export tally to CSV"""
        import csv

        tally = self.tallies[tally_number]

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow(['Tally', tally_number])
            writer.writerow(['NPS', self.header['nps']])
            writer.writerow([])

            # Column headers
            headers = ['Bin', 'Energy_Min', 'Energy_Max', 'Value', 'Rel_Error', 'Abs_Error']
            writer.writerow(headers)

            # Data rows
            for i, (val, err) in enumerate(zip(tally['values'], tally['errors'])):
                if i < len(tally['values']) - 1:  # Skip total (last entry)
                    e_bin_idx = i % tally['n_energy_bins']
                    e_min = tally['energy_bins'][e_bin_idx]
                    e_max = tally['energy_bins'][e_bin_idx + 1]
                    abs_err = val * err

                    writer.writerow([i+1, f'{e_min:.4e}', f'{e_max:.4e}',
                                   f'{val:.4e}', f'{err:.4f}', f'{abs_err:.4e}'])

            # Total row
            writer.writerow(['TOTAL', '', '',
                           f'{tally["values"][-1]:.4e}',
                           f'{tally["errors"][-1]:.4f}',
                           f'{tally["values"][-1] * tally["errors"][-1]:.4e}'])

        print(f"Exported tally {tally_number} to {output_file}")

    def export_to_excel(self, output_file):
        """Export all tallies to Excel workbook"""
        try:
            import pandas as pd
        except ImportError:
            print("pandas required for Excel export: pip install pandas openpyxl")
            return

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = {
                'Property': ['Code', 'Version', 'Problem ID', 'NPS', 'Random Seed', 'Number of Tallies'],
                'Value': [
                    self.header['code'],
                    self.header['version'],
                    self.header['probid'],
                    self.header['nps'],
                    self.header['random_seed'],
                    len(self.tallies)
                ]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)

            # Sheet per tally
            for tnum, tally in self.tallies.items():
                data = {
                    'Bin': range(1, len(tally['values'])),
                    'Value': tally['values'][:-1],  # Exclude total
                    'Rel_Error': tally['errors'][:-1],
                    'Abs_Error': [v*e for v, e in zip(tally['values'][:-1], tally['errors'][:-1])]
                }

                if 'energy_bins' in tally and len(tally['energy_bins']) > 2:
                    # Add energy bin boundaries
                    n_e = tally['n_energy_bins']
                    data['E_min'] = [tally['energy_bins'][i % n_e]
                                     for i in range(len(tally['values'])-1)]
                    data['E_max'] = [tally['energy_bins'][(i % n_e) + 1]
                                     for i in range(len(tally['values'])-1)]

                df = pd.DataFrame(data)
                sheet_name = f'Tally_{tnum}'[:31]  # Excel limit
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Exported to Excel: {output_file}")

    def merge_mctal_files(self, filepaths, output_file, method='average'):
        """
        Merge multiple MCTAL files

        Args:
            filepaths: List of MCTAL file paths
            output_file: Output merged MCTAL path
            method: 'average' (history-weighted) or 'sum'

        Note: Files must have identical tally structure
        """

        # Parse all files
        processors = []
        for fpath in filepaths:
            proc = MCTALProcessor()
            proc.parse_file(fpath)
            processors.append(proc)

        # Verify compatibility
        tally_nums = set(processors[0].tallies.keys())
        for proc in processors[1:]:
            if set(proc.tallies.keys()) != tally_nums:
                raise ValueError("Tallies must match across all MCTAL files")

        # Merge tallies
        merged = MCTALProcessor()
        merged.header = processors[0].header.copy()

        total_nps = sum(p.header['nps'] for p in processors)
        merged.header['nps'] = total_nps

        for tnum in tally_nums:
            merged_tally = processors[0].tallies[tnum].copy()
            n_bins = len(merged_tally['values'])

            if method == 'average':
                # History-weighted average
                weights = [p.header['nps'] / total_nps for p in processors]

                merged_values = np.zeros(n_bins)
                merged_errors_sq = np.zeros(n_bins)

                for proc, weight in zip(processors, weights):
                    tally = proc.tallies[tnum]
                    merged_values += weight * np.array(tally['values'])
                    # Variance combination: σ²_total = Σ w_i² σ_i²
                    errors_sq = (np.array(tally['values']) * np.array(tally['errors']))**2
                    merged_errors_sq += (weight ** 2) * errors_sq

                # Convert back to relative errors
                merged_tally['values'] = merged_values.tolist()
                merged_errors = np.sqrt(merged_errors_sq)
                merged_tally['errors'] = (merged_errors / merged_values).tolist()

            elif method == 'sum':
                # Direct sum (for independent samples)
                merged_tally['values'] = np.sum([np.array(p.tallies[tnum]['values'])
                                                 for p in processors], axis=0).tolist()
                # Error combination for sums: σ_sum = √(Σ σ_i²)
                errors_sq_sum = np.sum([
                    (np.array(p.tallies[tnum]['values']) * np.array(p.tallies[tnum]['errors']))**2
                    for p in processors], axis=0)
                merged_errors = np.sqrt(errors_sq_sum)
                merged_tally['errors'] = (merged_errors / np.array(merged_tally['values'])).tolist()

            merged.tallies[tnum] = merged_tally

        # Write merged MCTAL
        self._write_mctal(merged, output_file)

        print(f"Merged {len(filepaths)} MCTAL files → {output_file}")
        print(f"Method: {method}, Total NPS: {total_nps}")

        return merged

    def _write_mctal(self, processor, output_file):
        """Write MCTAL file in standard format"""

        with open(output_file, 'w') as f:
            # Header
            f.write(f"{processor.header['code']}    {processor.header['version']}    {processor.header['probid']}\n")

            # Counts
            n_tallies = len(processor.tallies)
            f.write(f"     2     {n_tallies}     1     0  ntal npert\n")

            # NPS and random
            f.write(f"   {processor.header['nps']}  {processor.header.get('random_seed', 0)}  nps rnr\n")

            # Write each tally
            for tnum, tally in processor.tallies.items():
                # Descriptor
                f.write(f"      {tally['number']}  {tally['detector_flag']}  {tally['user_flag']}  "
                       f"{tally['segment_flag']}  {tally['multiplier_flag']}  {tally['cosine_flag']}  "
                       f"{tally['energy_flag']}  {tally['time_flag']}\n")

                # Cells
                f.write(f"     {len(tally['cells'])}  ")
                f.write("  ".join(str(c) for c in tally['cells']))
                f.write("\n")

                # Energy bins
                if tally['energy_flag']:
                    f.write(f"     {tally['n_energy_bins']}\n")
                    for ebin in tally['energy_bins']:
                        f.write(f"  {ebin:.6E}")
                    f.write("\n")

                # Values and errors
                for val, err in zip(tally['values'], tally['errors']):
                    f.write(f" {val:.6E}  {err:.4f}\n")

        print(f"Written MCTAL file: {output_file}")
```

### Step 4: Common Operations

**Extract specific tally:**
```python
processor = MCTALProcessor()
processor.parse_file('mctal')

tally_4 = processor.get_tally(4)

print(f"Tally {tally_4['number']}")
print(f"Energy bins: {len(tally_4['energy_bins'])-1}")
print(f"Total flux: {tally_4['values'][-1]:.4e}")
print(f"Relative error: {tally_4['errors'][-1]:.2%}")
```

**Export to CSV:**
```python
processor.export_to_csv(tally_number=4, output_file='tally4.csv')
# Creates CSV with columns: Bin, Energy_Min, Energy_Max, Value, Rel_Error, Abs_Error
```

**Export to Excel:**
```python
processor.export_to_excel('all_tallies.xlsx')
# Creates workbook with Summary sheet + one sheet per tally
```

**Merge parameter study results:**
```python
mctal_files = ['run1/mctal', 'run2/mctal', 'run3/mctal', 'run4/mctal']

merged = processor.merge_mctal_files(
    filepaths=mctal_files,
    output_file='merged_mctal',
    method='average'  # History-weighted average
)

# Now merged MCTAL contains averaged results
# Can export or further analyze
merged.export_to_csv(4, 'averaged_tally4.csv')
```

## Integration with Other Skills

After MCTAL processing:

- **mcnp-tally-analyzer**: Analyze/interpret extracted tally data
- **mcnp-plotter**: Create plots from exported CSV/DataFrame
- **mcnp-statistics-checker**: Validate TFC data from MCTAL
- **mcnp-output-parser**: Cross-check with OUTP file for validation

## Important Processing Principles

1. **MCTAL vs OUTP**
   - MCTAL is machine-readable, OUTP is human-readable
   - MCTAL easier to parse programmatically
   - OUTP has more context and explanations
   - Both should agree (cross-validation)

2. **File integrity**
   - Check header NPS matches expected
   - Verify all tallies present
   - Check for truncation (incomplete runs)

3. **Merging requirements**
   - Files must have identical tally structure
   - Use history-weighted averaging (not simple mean)
   - Combine errors correctly (variance addition)

4. **Error propagation**
   - Relative errors are fractional (not %)
   - Absolute error = value × relative_error
   - Combined variance = Σ(σ_i²) for sums
   - Weighted variance for averages

5. **Export formats**
   - CSV: Simple, universal, but loses structure
   - Excel: Multi-sheet preserves organization
   - HDF5: Efficient for large datasets
   - JSON: Web-friendly, structured

6. **Performance**
   - MCTAL files can be large (GB for mesh tallies)
   - Parse incrementally for very large files
   - Use binary formats (HDF5) for big data

## Example Workflows

### Example 1: Export Tally for Excel Analysis

```
User: "I need to get my F4 tally data into Excel"

Claude: I'll parse your MCTAL file and export tally 4 to Excel format.

[Uses MCTALProcessor]

```python
from mcnp_mctal_processor import MCTALProcessor

# Parse MCTAL
processor = MCTALProcessor()
data = processor.parse_file('mctal')

# Export tally 4 to CSV (Excel can open)
processor.export_to_csv(tally_number=4, output_file='tally4.csv')

# OR export all tallies to Excel workbook
processor.export_to_excel('all_tallies.xlsx')
```

**Results:**

✓ Created `tally4.csv`:
  - Columns: Bin, Energy_Min, Energy_Max, Value, Rel_Error, Abs_Error
  - 5 energy bins + 1 total row
  - Ready to open in Excel

✓ Created `all_tallies.xlsx`:
  - Sheet 1: Summary (run info, NPS, tallies)
  - Sheet 2: Tally_4 (flux data)
  - Sheet 3: Tally_14 (mesh data)
  - ... (one sheet per tally)

**To use in Excel:**
1. Open tally4.csv or all_tallies.xlsx
2. Create charts (Insert → Chart → Scatter)
3. Plot Value vs Energy bins
4. Add error bars from Abs_Error column
5. Format as needed for reports

Would you like me to:
1. Show how to create plots in Excel?
2. Export specific energy bins only?
3. Merge with other runs?
```

### Example 2: Merge Parameter Study Results

```
User: "I ran 10 cases varying shield thickness. Merge the results."

Claude: I'll merge your 10 MCTAL files using history-weighted averaging.

[Uses MCTALProcessor]

```python
from mcnp_mctal_processor import MCTALProcessor
import glob

# Find all MCTAL files
mctal_files = glob.glob('case_*/mctal')  # Assumes case_1/, case_2/, ... directories
print(f"Found {len(mctal_files)} MCTAL files")

# Merge with history-weighted averaging
processor = MCTALProcessor()
merged = processor.merge_mctal_files(
    filepaths=mctal_files,
    output_file='merged_all_cases.mctal',
    method='average'  # Weight by NPS from each run
)

# Export merged results
merged.export_to_excel('merged_results.xlsx')

# Summary statistics
for tnum in [4, 14]:  # F4 and F14 tallies
    tally = merged.get_tally(tnum)
    total = tally['values'][-1]
    error = tally['errors'][-1]

    print(f"Tally F{tnum}:")
    print(f"  Merged value: {total:.4e}")
    print(f"  Merged error: {error:.2%}")
    print(f"  Combined NPS: {merged.header['nps']}")
```

**Output:**

Merging 10 MCTAL files...
  case_1/mctal: 100,000 NPS
  case_2/mctal: 100,000 NPS
  ...
  case_10/mctal: 100,000 NPS

Merged 10 MCTAL files → merged_all_cases.mctal
Method: average, Total NPS: 1,000,000

Tally F4:
  Merged value: 2.73E-04
  Merged error: 1.01% (improved from ~3.2% individual runs)
  Combined NPS: 1,000,000

Tally F14:
  Merged value: 3.45E-05
  Merged error: 3.98% (improved from ~12.5%)
  Combined NPS: 1,000,000

**Analysis:**
- Merging 10 runs improved statistics by √10 ≈ 3.16×
- Individual run errors ~3.2% → merged ~1.0% ✓
- Can now use merged results for production analysis
- Uncertainty reduction confirms statistical independence of runs

Would you like me to:
1. Plot comparison of individual vs merged results?
2. Export merged data for further analysis?
3. Create summary table across all cases?
```

## Code Style Guidelines

When processing MCTAL files:
- Validate file format before parsing
- Handle missing TFC data gracefully
- Check array dimensions match expectations
- Use vectorized operations (numpy) for large datasets
- Close files properly (use context managers)
- Provide progress indicators for large files

## Dependencies

**Required Python packages:**
- `numpy` - Array operations
- Standard library: `re`, `csv`

**Optional packages:**
- `pandas` - DataFrame export, Excel writing
- `openpyxl` - Excel file format support
- `h5py` - HDF5 export for large datasets

**Required components:**
- Reference: `.claude/commands/mcnp-mctal-processor.md` (detailed procedures)

## References

**Primary References:**
- `.claude/commands/mcnp-mctal-processor.md` - Complete processing procedures
- `COMPLETE_MCNP6_KNOWLEDGE_BASE.md` - MCTAL format section
- Chapter 5.9: Tally specification (defines MCTAL contents)

**MCTAL Format:**
- MCNP manual appendix: MCTAL file format specification
- Header structure and tally block format
- TFC (Tally Fluctuation Chart) data structure

**Related Skills:**
- mcnp-output-parser: Alternative parsing from OUTP
- mcnp-tally-analyzer: Interpret extracted data
- mcnp-plotter: Visualize exported data
- mcnp-statistics-checker: Validate TFC data

"""
MCNP6 Output File Parser
Comprehensive parser for MCNP6.3 output files (OUTP, MCTAL, MESHTAL)
"""

import re
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


@dataclass
class TallyResult:
    """Represents a tally result from MCNP output"""
    tally_number: int
    tally_type: str
    particle_type: str
    bins: List[Dict[str, Any]] = field(default_factory=list)
    values: List[float] = field(default_factory=list)
    errors: List[float] = field(default_factory=list)
    statistical_checks: Dict[str, bool] = field(default_factory=dict)
    figure_of_merit: float = 0.0


@dataclass
class KCODEResult:
    """Represents KCODE criticality results"""
    k_combined: Tuple[float, float] = (0.0, 0.0)  # (keff, sigma)
    k_collision: Tuple[float, float] = (0.0, 0.0)
    k_absorption: Tuple[float, float] = (0.0, 0.0)
    k_track_length: Tuple[float, float] = (0.0, 0.0)
    cycles: int = 0
    inactive_cycles: int = 0
    active_cycles: int = 0
    particles_per_cycle: int = 0
    cycle_values: List[float] = field(default_factory=list)
    shannon_entropy: List[float] = field(default_factory=list)


@dataclass
class Warning:
    """Represents a warning message"""
    message: str
    line_number: int = 0
    category: str = "general"


@dataclass
class FatalError:
    """Represents a fatal error"""
    message: str
    line_number: int = 0
    card_type: str = ""
    card_number: Optional[int] = None


class MCNPOutputParser:
    """
    Comprehensive MCNP6 output file parser
    
    Handles:
    - Problem summary (cells, surfaces, materials)
    - Warning and error messages
    - Tally results with statistics
    - KCODE criticality results
    - Computer time summary
    - Statistical quality checks
    """
    
    def __init__(self):
        self.warnings: List[Warning] = []
        self.errors: List[FatalError] = []
        self.tallies: Dict[int, TallyResult] = {}
        self.kcode_result: Optional[KCODEResult] = None
        self.problem_summary: Dict[str, Any] = {}
        self.computer_time: Dict[str, float] = {}
        self.run_terminated_normally = False
        
    def parse_file(self, filepath: str) -> Dict[str, Any]:
        """
        Parse MCNP output file
        
        Args:
            filepath: Path to MCNP output file (usually 'outp')
            
        Returns:
            Dictionary with parsed results
        """
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        return self.parse_string(content)
    
    def parse_string(self, content: str) -> Dict[str, Any]:
        """Parse MCNP output from string"""
        lines = content.split('\n')
        
        # Parse different sections
        self._parse_warnings_errors(lines)
        self._parse_problem_summary(lines)
        self._parse_tallies(lines)
        self._parse_kcode(lines)
        self._parse_computer_time(lines)
        self._check_normal_termination(lines)
        
        return {
            'warnings': self.warnings,
            'errors': self.errors,
            'tallies': self.tallies,
            'kcode': self.kcode_result,
            'problem_summary': self.problem_summary,
            'computer_time': self.computer_time,
            'terminated_normally': self.run_terminated_normally
        }
    
    def _parse_warnings_errors(self, lines: List[str]):
        """Extract warning and error messages"""
        for i, line in enumerate(lines):
            line_upper = line.upper()
            
            # Fatal errors
            if 'FATAL ERROR' in line_upper or 'BAD TROUBLE' in line_upper:
                # Extract error details
                error_msg = line.strip()
                # Try to get more context
                if i + 1 < len(lines):
                    error_msg += " " + lines[i+1].strip()
                
                self.errors.append(FatalError(
                    message=error_msg,
                    line_number=i+1
                ))
            
            # Warnings
            elif 'WARNING' in line_upper:
                category = "general"
                if 'GEOMETRY' in line_upper:
                    category = "geometry"
                elif 'MATERIAL' in line_upper:
                    category = "material"
                elif 'TALLY' in line_upper:
                    category = "tally"
                elif 'SOURCE' in line_upper:
                    category = "source"
                
                self.warnings.append(Warning(
                    message=line.strip(),
                    line_number=i+1,
                    category=category
                ))
    
    def _parse_problem_summary(self, lines: List[str]):
        """Parse problem summary section"""
        in_summary = False
        
        for line in lines:
            if '1PROBLEM SUMMARY' in line:
                in_summary = True
                continue
            
            if in_summary:
                # Extract problem statistics
                if 'CELLS' in line and 'SURFACES' in line:
                    parts = line.split()
                    try:
                        self.problem_summary['cells'] = int(parts[1])
                        self.problem_summary['surfaces'] = int(parts[3])
                    except (ValueError, IndexError):
                        pass
                
                if 'MATERIALS' in line:
                    try:
                        self.problem_summary['materials'] = int(line.split()[1])
                    except (ValueError, IndexError):
                        pass
                
                if 'TOTAL NU' in line.upper():
                    try:
                        self.problem_summary['total_nu'] = float(line.split()[-1])
                    except (ValueError, IndexError):
                        pass
                
                # End of summary
                if line.startswith('1'):
                    in_summary = False
    
    def _parse_tallies(self, lines: List[str]):
        """Parse tally results and statistical checks"""
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Look for tally headers
            tally_match = re.search(r'tally\s+(\d+)', line, re.IGNORECASE)
            if tally_match:
                tally_num = int(tally_match.group(1))
                
                # Determine tally type
                tally_type = self._extract_tally_type(line)
                
                # Determine particle type
                particle = self._extract_particle_type(line)
                
                # Parse tally data
                tally_data = self._parse_tally_data(lines, i)
                
                # Parse statistical checks
                stats = self._parse_statistical_checks(lines, i)
                
                self.tallies[tally_num] = TallyResult(
                    tally_number=tally_num,
                    tally_type=tally_type,
                    particle_type=particle,
                    values=tally_data.get('values', []),
                    errors=tally_data.get('errors', []),
                    bins=tally_data.get('bins', []),
                    statistical_checks=stats,
                    figure_of_merit=tally_data.get('fom', 0.0)
                )
            
            i += 1
    
    def _extract_tally_type(self, line: str) -> str:
        """Extract tally type from header line"""
        line_lower = line.lower()
        if 'surface current' in line_lower:
            return 'F1'
        elif 'surface flux' in line_lower:
            return 'F2'
        elif 'track length' in line_lower:
            return 'F4'
        elif 'point detector' in line_lower or 'ring detector' in line_lower:
            return 'F5'
        elif 'energy deposition' in line_lower:
            return 'F6'
        elif 'fission energy' in line_lower:
            return 'F7'
        elif 'pulse height' in line_lower:
            return 'F8'
        else:
            return 'unknown'
    
    def _extract_particle_type(self, line: str) -> str:
        """Extract particle type from tally line"""
        particles = ['neutron', 'photon', 'electron', 'proton']
        for p in particles:
            if p in line.lower():
                return p[0]  # Return first letter
        return 'n'  # Default to neutron
    
    def _parse_tally_data(self, lines: List[str], start_idx: int) -> Dict[str, Any]:
        """Parse tally values and errors from output"""
        values = []
        errors = []
        bins = []
        fom = 0.0
        
        # Look ahead for tally table
        for i in range(start_idx, min(start_idx + 200, len(lines))):
            line = lines[i].strip()
            
            # Skip empty and header lines
            if not line or 'tally' in line.lower() or '---' in line:
                continue
            
            # Look for numerical data (energy bin, value, error)
            parts = line.split()
            if len(parts) >= 2:
                try:
                    # Try to parse as float
                    value = float(parts[-2])
                    error = float(parts[-1])
                    values.append(value)
                    errors.append(error)
                    
                    # Try to get bin information
                    if len(parts) >= 3:
                        bin_value = float(parts[0])
                        bins.append({'energy': bin_value, 'value': value, 'error': error})
                except (ValueError, IndexError):
                    pass
            
            # Look for figure of merit
            if 'figure of merit' in line.lower():
                try:
                    fom = float(line.split()[-1])
                except ValueError:
                    pass
            
            # Stop at next section
            if 'tally fluctuation' in line.lower() or \
               'the tally' in line.lower() or \
               'dump no.' in line.lower():
                break
        
        return {
            'values': values,
            'errors': errors,
            'bins': bins,
            'fom': fom
        }
    
    def _parse_statistical_checks(self, lines: List[str], start_idx: int) -> Dict[str, bool]:
        """Parse the 10 statistical checks for tally quality"""
        checks = {}
        
        # Look for tally fluctuation chart section
        for i in range(start_idx, min(start_idx + 300, len(lines))):
            line = lines[i]
            
            if 'tally fluctuation chart' in line.lower():
                # Next lines contain the 10 checks
                for j in range(i+1, min(i+20, len(lines))):
                    check_line = lines[j]
                    
                    # Look for "passed" or "not passed"
                    if 'passed' in check_line.lower():
                        # Extract check number
                        match = re.search(r'(\d+)', check_line)
                        if match:
                            check_num = int(match.group(1))
                            passed = 'not passed' not in check_line.lower()
                            checks[f'check_{check_num}'] = passed
                
                break
        
        return checks
    
    def _parse_kcode(self, lines: List[str]):
        """Parse KCODE criticality results"""
        kcode_data = KCODEResult()
        
        for i, line in enumerate(lines):
            # Look for final k-effective results
            if 'the final estimated' in line.lower() and 'combined' in line.lower():
                # Next lines contain k-eff values
                for j in range(i, min(i+10, len(lines))):
                    l = lines[j]
                    
                    if 'col/abs/tl keff' in l.lower() or 'combined' in l.lower():
                        # Extract k-eff and sigma
                        parts = l.split()
                        for k, part in enumerate(parts):
                            try:
                                if '.' in part and float(part) > 0.5 and float(part) < 2.0:
                                    keff = float(part)
                                    if k+1 < len(parts):
                                        sigma = float(parts[k+1])
                                        kcode_data.k_combined = (keff, sigma)
                                    break
                            except ValueError:
                                pass
            
            # Look for cycle information
            if 'kcode' in line.lower() and 'cycles' in line.lower():
                try:
                    parts = line.split()
                    # Extract cycle counts
                    for j, part in enumerate(parts):
                        if part.isdigit():
                            if 'skip' in line.lower() or 'inactive' in line.lower():
                                kcode_data.inactive_cycles = int(part)
                            elif kcode_data.cycles == 0:
                                kcode_data.cycles = int(part)
                except ValueError:
                    pass
            
            # Collect cycle-by-cycle k-eff
            if 'cycle' in line.lower() and 'k(collision)' in line.lower():
                # Parse k-eff values from table
                for j in range(i+1, min(i+200, len(lines))):
                    cycle_line = lines[j].strip()
                    if not cycle_line or 'average' in cycle_line.lower():
                        break
                    
                    parts = cycle_line.split()
                    if len(parts) >= 2:
                        try:
                            cycle_num = int(parts[0])
                            k_value = float(parts[1])
                            kcode_data.cycle_values.append(k_value)
                        except ValueError:
                            break
        
        if kcode_data.k_combined[0] > 0:
            kcode_data.active_cycles = len(kcode_data.cycle_values) - kcode_data.inactive_cycles
            self.kcode_result = kcode_data
    
    def _parse_computer_time(self, lines: List[str]):
        """Parse computer time summary"""
        for i, line in enumerate(lines):
            if 'computer time' in line.lower() and '=' in line:
                # Extract time values
                parts = line.split('=')
                if len(parts) >= 2:
                    try:
                        time_str = parts[1].split()[0]
                        time_val = float(time_str)
                        
                        if 'total' in line.lower():
                            self.computer_time['total'] = time_val
                        elif 'source' in line.lower():
                            self.computer_time['source'] = time_val
                        elif 'track' in line.lower():
                            self.computer_time['tracking'] = time_val
                    except (ValueError, IndexError):
                        pass
    
    def _check_normal_termination(self, lines: List[str]):
        """Check if run terminated normally"""
        for line in lines:
            if 'run terminated' in line.lower() and 'mcnp' in line.lower():
                self.run_terminated_normally = True
                break
    
    def get_worst_tally_error(self) -> Tuple[Optional[int], float]:
        """Get tally with worst (highest) relative error"""
        worst_tally = None
        worst_error = 0.0
        
        for tally_num, tally in self.tallies.items():
            if tally.errors:
                max_error = max(tally.errors)
                if max_error > worst_error:
                    worst_error = max_error
                    worst_tally = tally_num
        
        return worst_tally, worst_error
    
    def get_failed_statistical_checks(self) -> Dict[int, List[str]]:
        """Get tallies with failed statistical checks"""
        failed = {}
        
        for tally_num, tally in self.tallies.items():
            failed_checks = [check for check, passed in tally.statistical_checks.items() if not passed]
            if failed_checks:
                failed[tally_num] = failed_checks
        
        return failed
    
    def has_fatal_errors(self) -> bool:
        """Check if output contains fatal errors"""
        return len(self.errors) > 0
    
    def get_k_effective(self) -> Tuple[float, float]:
        """Get k-effective value and uncertainty"""
        if self.kcode_result:
            return self.kcode_result.k_combined
        return (0.0, 0.0)


class MCTALParser:
    """
    Parser for MCTAL files (tally output files)
    Supports both ASCII and binary formats
    """
    
    def __init__(self):
        self.tallies = {}
        self.header = {}
    
    def parse_file(self, filepath: str) -> Dict[str, Any]:
        """Parse MCTAL file"""
        # Try ASCII first
        try:
            return self._parse_ascii(filepath)
        except:
            # Try binary
            return self._parse_binary(filepath)
    
    def _parse_ascii(self, filepath: str) -> Dict[str, Any]:
        """Parse ASCII MCTAL format"""
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Parse header
        if lines:
            header_parts = lines[0].split()
            self.header = {
                'code': header_parts[0] if len(header_parts) > 0 else '',
                'version': header_parts[1] if len(header_parts) > 1 else '',
                'date': ' '.join(header_parts[2:5]) if len(header_parts) > 4 else ''
            }
        
        # Parse tally data
        i = 1
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for tally number
            if line.startswith('tally'):
                parts = line.split()
                tally_num = int(parts[1])
                
                # Parse tally details (simplified)
                tally_data = {
                    'number': tally_num,
                    'values': [],
                    'errors': []
                }
                
                # Skip to data section
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('tally'):
                    data_line = lines[i].strip()
                    if data_line:
                        try:
                            parts = data_line.split()
                            if len(parts) >= 2:
                                tally_data['values'].append(float(parts[0]))
                                tally_data['errors'].append(float(parts[1]))
                        except ValueError:
                            pass
                    i += 1
                
                self.tallies[tally_num] = tally_data
            else:
                i += 1
        
        return {
            'header': self.header,
            'tallies': self.tallies
        }
    
    def _parse_binary(self, filepath: str) -> Dict[str, Any]:
        """Parse binary MCTAL format (simplified placeholder)"""
        # Binary MCTAL parsing requires struct module and format specification
        # This is a placeholder - full implementation would handle binary format
        return {
            'header': {},
            'tallies': {},
            'format': 'binary',
            'note': 'Binary MCTAL parsing not yet fully implemented'
        }


if __name__ == "__main__":
    # Test the output parser
    parser = MCNPOutputParser()
    
    # Test with sample output
    test_output = """
    warning. cell 10 is not used.
    fatal error. bad trouble in subroutine sourcc
    
    tally 4   neutron track length
    cell 10    energy 1.0000E+00    value 1.2345E-02    error 0.0234
    
    the final estimated combined keff = 1.00234 with sigma = 0.00123
    
    run terminated when 1000000 particle histories were done.
    """
    
    result = parser.parse_string(test_output)
    print(f"Found {len(result['warnings'])} warnings, {len(result['errors'])} errors")
    print(f"Parsed {len(result['tallies'])} tallies")
    if result['kcode']:
        print(f"k-eff = {result['kcode'].k_combined[0]:.5f} ± {result['kcode'].k_combined[1]:.5f}")

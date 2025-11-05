"""
Error Pattern Database
Common MCNP errors, warnings, and fixes
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import re


@dataclass
class ErrorPattern:
    """Represents a known error pattern"""
    pattern: str  # Regex pattern to match error
    category: str
    severity: str  # 'fatal', 'warning', 'info'
    description: str
    cause: str
    fix: str
    example: Optional[str] = None


class ErrorPatternDatabase:
    """
    Database of common MCNP errors and their solutions
    """
    
    def __init__(self):
        self.patterns: List[ErrorPattern] = []
        self._load_patterns()
    
    def _load_patterns(self):
        """Load all known error patterns"""
        
        # Fatal errors
        self.patterns.extend([
            ErrorPattern(
                pattern=r"bad trouble in subroutine sourcc",
                category="source",
                severity="fatal",
                description="Source particle location invalid",
                cause="Source positioned outside defined geometry or in void cell",
                fix="Check SDEF position coordinates. Ensure source is in a non-void cell with importance > 0.",
                example="sdef pos=0 0 0  $ Verify (0,0,0) is inside geometry"
            ),
            ErrorPattern(
                pattern=r"source particle type .+ not on mode card",
                category="source",
                severity="fatal",
                description="Particle type mismatch",
                cause="MODE card doesn't include source particle type",
                fix="Add particle type to MODE card (e.g., MODE N P for neutron and photon)",
                example="mode n p  $ For neutron and photon transport"
            ),
            ErrorPattern(
                pattern=r"lost particle",
                category="geometry",
                severity="fatal",
                description="Particle tracking lost in geometry",
                cause="Geometry gaps, overlaps, or undefined regions",
                fix="Check cell definitions for gaps. Use geometry plotter to visualize. Ensure all space is defined.",
                example="Use: mcnp6 ip name=input.i  # Run geometry plotter"
            ),
            ErrorPattern(
                pattern=r"geometry error",
                category="geometry",
                severity="fatal",
                description="Invalid geometry specification",
                cause="Cell/surface definition error, missing surfaces, or invalid boolean logic",
                fix="Check cell card geometry expressions. Verify all referenced surfaces exist.",
                example="10 1 -2.7 -1 2 -3  $ Ensure surfaces 1, 2, 3 are defined"
            ),
            ErrorPattern(
                pattern=r"duplicate card",
                category="input",
                severity="fatal",
                description="Card specified multiple times",
                cause="Same card appears twice in input",
                fix="Remove duplicate card. Check for copy-paste errors.",
                example="# Remove duplicate material or tally definitions"
            ),
            ErrorPattern(
                pattern=r"bad cell number",
                category="geometry",
                severity="fatal",
                description="Invalid cell reference",
                cause="Cell number referenced doesn't exist or is invalid",
                fix="Check cell numbers in tallies, importance cards, etc. Ensure cell exists.",
                example="f4:n 10  $ Verify cell 10 exists in cell block"
            ),
            ErrorPattern(
                pattern=r"surface .+ undefined",
                category="geometry",
                severity="fatal",
                description="Missing surface definition",
                cause="Cell references a surface that doesn't exist",
                fix="Add missing surface card or correct surface number in cell definition",
                example="1 so 10  $ Add this surface definition"
            ),
            ErrorPattern(
                pattern=r"xsdir file not found",
                category="data",
                severity="fatal",
                description="Cross-section directory missing",
                cause="DATAPATH not set or xsdir file missing",
                fix="Set DATAPATH environment variable pointing to cross-section library location",
                example="export DATAPATH=/path/to/mcnp/data"
            ),
            ErrorPattern(
                pattern=r"model required",
                category="physics",
                severity="fatal",
                description="Physics model needed but disabled",
                cause="Particle energy or type requires model physics (CEM, LAQGSM, etc.)",
                fix="Add MPHYS ON to enable model physics",
                example="mphys on  $ Enable physics models"
            ),
        ])
        
        # Warnings
        self.patterns.extend([
            ErrorPattern(
                pattern=r"cell .+ is not used",
                category="geometry",
                severity="warning",
                description="Unused cell definition",
                cause="Cell defined but not part of geometry",
                fix="Remove unused cell or include it in geometry definition",
                example="# Either use the cell or delete its definition"
            ),
            ErrorPattern(
                pattern=r"surface .+ not used",
                category="geometry",
                severity="warning",
                description="Unused surface definition",
                cause="Surface defined but not referenced by any cell",
                fix="Remove unused surface definition",
                example="# Delete unreferenced surface cards"
            ),
            ErrorPattern(
                pattern=r"cells .+ and .+ overlap",
                category="geometry",
                severity="warning",
                description="Overlapping cells detected",
                cause="Cell definitions result in overlapping regions",
                fix="Check boolean logic in cell definitions. Use # for complement if needed.",
                example="10 1 -2.7 -1 #20  $ Use complement to avoid overlap"
            ),
            ErrorPattern(
                pattern=r"material .+ not used",
                category="material",
                severity="warning",
                description="Unused material definition",
                cause="Material defined but not assigned to any cell",
                fix="Remove unused material or assign to a cell",
                example="# Delete unused M card"
            ),
            ErrorPattern(
                pattern=r"zaid .+ not in library",
                category="material",
                severity="warning",
                description="Isotope not available",
                cause="Requested ZAID not in cross-section library",
                fix="Check xsdir for available ZAIDs. Use different library ID (e.g., .80c vs .70c)",
                example="m1 92235.80c 1.0  $ Try different library ID"
            ),
            ErrorPattern(
                pattern=r"no tracks in tally",
                category="tally",
                severity="warning",
                description="Tally has no particle contributions",
                cause="Tally location has zero importance or particles don't reach it",
                fix="Check importance map. Add variance reduction. Verify geometry.",
                example="imp:n 1 1 1 0  $ Ensure tally cell has importance > 0"
            ),
            ErrorPattern(
                pattern=r"poor statistics",
                category="tally",
                severity="warning",
                description="Tally has large uncertainties",
                cause="Insufficient particle histories or poor variance reduction",
                fix="Increase NPS. Add variance reduction (importance, weight windows). Check tally location.",
                example="nps 10000000  $ Increase particle count"
            ),
        ])
        
        # Statistical warnings
        self.patterns.extend([
            ErrorPattern(
                pattern=r"tally .+ failed statistical checks",
                category="statistics",
                severity="warning",
                description="Tally failed quality checks",
                cause="Insufficient histories, poor convergence, or biased sampling",
                fix="Increase NPS, improve variance reduction, check for tally fluctuations",
                example="nps 100000000  # More particles\nwwn:n 1 1 1 1  # Add weight windows"
            ),
            ErrorPattern(
                pattern=r"figure of merit decreasing",
                category="statistics",
                severity="warning",
                description="Computational efficiency degrading",
                cause="Variance reduction causing bias or too many short tracks",
                fix="Review variance reduction settings. Check weight cutoffs.",
                example="# Adjust IMP, WWE, or DXTRAN parameters"
            ),
        ])
    
    def match_error(self, error_message: str) -> List[ErrorPattern]:
        """
        Find patterns matching an error message
        
        Args:
            error_message: Error text from MCNP output
        
        Returns:
            List of matching error patterns
        """
        matches = []
        error_lower = error_message.lower()
        
        for pattern in self.patterns:
            if re.search(pattern.pattern, error_lower, re.IGNORECASE):
                matches.append(pattern)
        
        return matches
    
    def get_by_category(self, category: str) -> List[ErrorPattern]:
        """Get all patterns for a category"""
        return [p for p in self.patterns if p.category.lower() == category.lower()]
    
    def get_by_severity(self, severity: str) -> List[ErrorPattern]:
        """Get patterns by severity level"""
        return [p for p in self.patterns if p.severity.lower() == severity.lower()]
    
    def suggest_fix(self, error_message: str) -> Optional[str]:
        """
        Get suggested fix for an error
        
        Args:
            error_message: Error text
        
        Returns:
            Fix suggestion or None
        """
        matches = self.match_error(error_message)
        if matches:
            # Return fix from best match
            return matches[0].fix
        return None
    
    def get_all_fatal_errors(self) -> List[ErrorPattern]:
        """Get all known fatal error patterns"""
        return self.get_by_severity('fatal')
    
    def get_all_warnings(self) -> List[ErrorPattern]:
        """Get all known warning patterns"""
        return self.get_by_severity('warning')


if __name__ == "__main__":
    # Test error pattern database
    db = ErrorPatternDatabase()
    
    print(f"Loaded {len(db.patterns)} error patterns")
    print(f"Fatal errors: {len(db.get_all_fatal_errors())}")
    print(f"Warnings: {len(db.get_all_warnings())}")
    
    # Test matching
    test_errors = [
        "bad trouble in subroutine sourcc",
        "cell 10 is not used",
        "lost particle in cell 5"
    ]
    
    print("\n=== Testing Error Matching ===")
    for error in test_errors:
        matches = db.match_error(error)
        print(f"\nError: {error}")
        if matches:
            pattern = matches[0]
            print(f"  Category: {pattern.category}")
            print(f"  Severity: {pattern.severity}")
            print(f"  Fix: {pattern.fix}")

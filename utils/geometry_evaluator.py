"""
MCNP6 Geometry Evaluator
Evaluate CSG (Constructive Solid Geometry) expressions for cell definitions
"""

import re
from typing import List, Tuple, Set, Optional, Any
from dataclasses import dataclass
from enum import Enum


class OperatorType(Enum):
    INTERSECTION = "intersection"
    UNION = "union"
    COMPLEMENT = "complement"


@dataclass
class GeometryNode:
    """Node in geometry expression tree"""
    operator: Optional[OperatorType] = None
    surface_num: Optional[int] = None
    sense: Optional[bool] = None  # True = positive side, False = negative side
    children: List['GeometryNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class GeometryEvaluator:
    """
    Evaluate and manipulate MCNP geometry expressions
    
    Handles:
    - Boolean operators: intersection (space), union (:), complement (#)
    - Surface sense: +surface (positive), -surface (negative)
    - Parentheses for grouping
    - Cell complements (#cell)
    """
    
    def __init__(self):
        self.surfaces_referenced: Set[int] = set()
        self.cells_referenced: Set[int] = set()
    
    def parse_geometry(self, geom_string: str) -> GeometryNode:
        """
        Parse geometry expression into tree structure
        
        Args:
            geom_string: Geometry expression (e.g., "-1 2 -3 : 4")
        
        Returns:
            Root node of geometry tree
        """
        self.surfaces_referenced.clear()
        self.cells_referenced.clear()
        
        # Tokenize
        tokens = self._tokenize(geom_string)
        
        # Parse into tree
        tree = self._parse_tokens(tokens)
        
        return tree
    
    def _tokenize(self, geom_string: str) -> List[str]:
        """
        Tokenize geometry string
        
        Tokens: surface numbers (with +/-), operators (:), parentheses, #
        """
        tokens = []
        current_token = ""
        
        for char in geom_string:
            if char in " \t\n":
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            elif char in "():":
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(char)
            elif char == "#":
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(char)
            else:
                current_token += char
        
        if current_token:
            tokens.append(current_token)
        
        return tokens
    
    def _parse_tokens(self, tokens: List[str]) -> GeometryNode:
        """Parse token list into geometry tree"""
        if not tokens:
            return GeometryNode()
        
        # Handle union operator (:) - lowest precedence
        union_indices = [i for i, t in enumerate(tokens) if t == ':']
        if union_indices:
            # Split on union operators
            parts = []
            start = 0
            for idx in union_indices:
                parts.append(tokens[start:idx])
                start = idx + 1
            parts.append(tokens[start:])
            
            # Create union node
            node = GeometryNode(operator=OperatorType.UNION)
            for part in parts:
                if part:
                    node.children.append(self._parse_tokens(part))
            return node
        
        # Handle intersection (space) - higher precedence
        # Look for terms (surfaces or parenthesized groups)
        terms = self._extract_terms(tokens)
        
        if len(terms) == 1:
            return terms[0]
        
        # Create intersection node
        node = GeometryNode(operator=OperatorType.INTERSECTION)
        node.children = terms
        return node
    
    def _extract_terms(self, tokens: List[str]) -> List[GeometryNode]:
        """Extract individual terms from token list"""
        terms = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            # Parenthesized expression
            if token == '(':
                # Find matching closing parenthesis
                depth = 1
                j = i + 1
                while j < len(tokens) and depth > 0:
                    if tokens[j] == '(':
                        depth += 1
                    elif tokens[j] == ')':
                        depth -= 1
                    j += 1
                
                # Parse contents of parentheses
                inner_tokens = tokens[i+1:j-1]
                terms.append(self._parse_tokens(inner_tokens))
                i = j
            
            # Cell complement
            elif token == '#':
                # Next token should be cell number
                if i + 1 < len(tokens):
                    try:
                        cell_num = int(tokens[i+1])
                        self.cells_referenced.add(cell_num)
                        node = GeometryNode(operator=OperatorType.COMPLEMENT)
                        node.surface_num = cell_num  # Store cell number in surface_num field
                        terms.append(node)
                        i += 2
                    except ValueError:
                        i += 1
                else:
                    i += 1
            
            # Surface reference
            else:
                try:
                    # Parse surface number with optional +/- sense
                    if token.startswith('+') or token.startswith('-'):
                        sense = (token[0] == '+')
                        surf_num = int(token[1:])
                    else:
                        sense = False  # Default to negative side
                        surf_num = int(token)
                    
                    self.surfaces_referenced.add(abs(surf_num))
                    
                    node = GeometryNode(
                        surface_num=surf_num,
                        sense=sense
                    )
                    terms.append(node)
                except ValueError:
                    pass
                
                i += 1
        
        return terms
    
    def get_all_surfaces(self, geom_string: str) -> Set[int]:
        """Extract all surface numbers referenced in geometry"""
        self.parse_geometry(geom_string)
        return self.surfaces_referenced
    
    def get_all_cells(self, geom_string: str) -> Set[int]:
        """Extract all cell numbers referenced in geometry (cell complements)"""
        self.parse_geometry(geom_string)
        return self.cells_referenced
    
    def simplify_geometry(self, geom_string: str) -> str:
        """
        Simplify geometry expression (basic simplification)
        
        - Remove redundant parentheses
        - Normalize spacing
        """
        tokens = self._tokenize(geom_string)
        
        # Rebuild with consistent spacing
        result = []
        for i, token in enumerate(tokens):
            if token == ':':
                result.append(' : ')
            elif token == '(':
                result.append('(')
            elif token == ')':
                result.append(')')
            elif token == '#':
                result.append('#')
            else:
                if result and result[-1] not in ['(', '#', ' : ']:
                    result.append(' ')
                result.append(token)
        
        return ''.join(result).strip()
    
    def negate_surface(self, surf_ref: str) -> str:
        """
        Negate a surface reference
        
        Args:
            surf_ref: Surface reference like "1", "-1", "+1"
        
        Returns:
            Negated reference
        """
        if surf_ref.startswith('+'):
            return '-' + surf_ref[1:]
        elif surf_ref.startswith('-'):
            return '+' + surf_ref[1:]
        else:
            # Default sense is negative, so negate to positive
            return '+' + surf_ref
    
    def substitute_surface(self, geom_string: str, old_surf: int, new_surf: int) -> str:
        """
        Replace all references to one surface with another
        
        Args:
            geom_string: Original geometry
            old_surf: Surface number to replace
            new_surf: Replacement surface number
        
        Returns:
            Modified geometry string
        """
        tokens = self._tokenize(geom_string)
        
        for i, token in enumerate(tokens):
            if token in [':', '(', ')', '#']:
                continue
            
            try:
                if token.startswith('+') or token.startswith('-'):
                    sign = token[0]
                    surf_num = int(token[1:])
                    if surf_num == old_surf:
                        tokens[i] = sign + str(new_surf)
                else:
                    surf_num = int(token)
                    if surf_num == old_surf:
                        tokens[i] = str(new_surf)
            except ValueError:
                pass
        
        return self.simplify_geometry(' '.join(tokens))
    
    def find_surface_sense(self, geom_string: str, surf_num: int) -> Optional[bool]:
        """
        Find the sense (+ or -) of a surface in geometry
        
        Args:
            geom_string: Geometry expression
            surf_num: Surface number to find
        
        Returns:
            True if positive sense, False if negative, None if not found
        """
        tokens = self._tokenize(geom_string)
        
        for token in tokens:
            if token in [':', '(', ')', '#']:
                continue
            
            try:
                if token.startswith('+'):
                    s_num = int(token[1:])
                    if s_num == surf_num:
                        return True
                elif token.startswith('-'):
                    s_num = int(token[1:])
                    if s_num == surf_num:
                        return False
                else:
                    s_num = int(token)
                    if s_num == surf_num:
                        return False  # Default is negative
            except ValueError:
                pass
        
        return None
    
    def is_valid_geometry(self, geom_string: str) -> Tuple[bool, str]:
        """
        Check if geometry expression is syntactically valid
        
        Returns:
            (is_valid, error_message)
        """
        try:
            tokens = self._tokenize(geom_string)
            
            # Check parentheses balance
            depth = 0
            for token in tokens:
                if token == '(':
                    depth += 1
                elif token == ')':
                    depth -= 1
                    if depth < 0:
                        return False, "Unmatched closing parenthesis"
            
            if depth != 0:
                return False, "Unmatched opening parenthesis"
            
            # Check for valid tokens
            for i, token in enumerate(tokens):
                if token in [':', '(', ')', '#']:
                    continue
                
                # Must be a number (with optional +/-)
                try:
                    if token.startswith('+') or token.startswith('-'):
                        int(token[1:])
                    else:
                        int(token)
                except ValueError:
                    return False, f"Invalid token: {token}"
            
            # Try to parse
            self.parse_geometry(geom_string)
            
            return True, ""
        
        except Exception as e:
            return False, str(e)
    
    def to_dnf(self, geom_string: str) -> str:
        """
        Convert geometry to Disjunctive Normal Form (union of intersections)
        
        This is a simplified version - full DNF conversion is complex.
        """
        # This would require full boolean algebra simplification
        # For now, just return normalized form
        return self.simplify_geometry(geom_string)


if __name__ == "__main__":
    # Test geometry evaluator
    evaluator = GeometryEvaluator()
    
    # Test 1: Simple intersection
    geom1 = "-1 2 -3"
    print(f"Geometry: {geom1}")
    surfaces = evaluator.get_all_surfaces(geom1)
    print(f"Surfaces referenced: {surfaces}")
    print(f"Simplified: {evaluator.simplify_geometry(geom1)}")
    print()
    
    # Test 2: Union
    geom2 = "-1 2 : 3 4"
    print(f"Geometry: {geom2}")
    surfaces = evaluator.get_all_surfaces(geom2)
    print(f"Surfaces referenced: {surfaces}")
    print()
    
    # Test 3: Cell complement
    geom3 = "#10 -20"
    print(f"Geometry: {geom3}")
    cells = evaluator.get_all_cells(geom3)
    surfaces = evaluator.get_all_surfaces(geom3)
    print(f"Cells referenced: {cells}")
    print(f"Surfaces referenced: {surfaces}")
    print()
    
    # Test 4: Validation
    geom4 = "-1 (2 : 3) 4"
    valid, msg = evaluator.is_valid_geometry(geom4)
    print(f"Geometry: {geom4}")
    print(f"Valid: {valid}, Message: {msg}")
    print()
    
    # Test 5: Surface substitution
    geom5 = "-1 2 -3"
    modified = evaluator.substitute_surface(geom5, 2, 99)
    print(f"Original: {geom5}")
    print(f"After substituting 2 → 99: {modified}")

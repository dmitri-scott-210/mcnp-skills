"""
MCNP6 Coordinate Transformations
Handle TR and TRCL cards for coordinate system transformations
"""

import numpy as np
from typing import Tuple, List, Optional
from dataclasses import dataclass


@dataclass
class TransformationMatrix:
    """Represents an MCNP transformation (TR card)"""
    translation: np.ndarray  # (x, y, z)
    rotation: np.ndarray     # 3x3 rotation matrix
    tr_number: int = 0
    is_displacement: bool = False  # False = main system to aux, True = aux to main
    
    def __init__(self, tr_number: int = 0):
        self.tr_number = tr_number
        self.translation = np.zeros(3)
        self.rotation = np.eye(3)
        self.is_displacement = False
    
    @classmethod
    def from_tr_card(cls, params: List[float], is_degrees: bool = False):
        """
        Create transformation from TR card parameters
        
        TR card format:
        - params[0:3]: displacement (x, y, z)
        - params[3:12]: rotation matrix or direction cosines
        - params[12]: optional m parameter (displacement flag)
        
        *TR uses degrees, TR uses direction cosines
        """
        trans = cls()
        
        if len(params) < 3:
            return trans
        
        # Translation
        trans.translation = np.array(params[0:3])
        
        # Rotation matrix
        if len(params) >= 12:
            # Full rotation matrix provided
            if is_degrees:
                # *TR format: angles in degrees
                # Convert to direction cosines
                trans.rotation = cls._angles_to_matrix(
                    params[3:6], params[6:9], params[9:12]
                )
            else:
                # TR format: direction cosines
                trans.rotation = np.array([
                    params[3:6],   # first row
                    params[6:9],   # second row
                    params[9:12]   # third row
                ])
        
        # Displacement flag
        if len(params) >= 13:
            trans.is_displacement = (params[12] == 1)
        
        return trans
    
    @staticmethod
    def _angles_to_matrix(v1: List[float], v2: List[float], v3: List[float]) -> np.ndarray:
        """Convert direction vectors to rotation matrix"""
        # Normalize vectors
        v1 = np.array(v1)
        v2 = np.array(v2)
        v3 = np.array(v3)
        
        v1 = v1 / np.linalg.norm(v1) if np.linalg.norm(v1) > 0 else v1
        v2 = v2 / np.linalg.norm(v2) if np.linalg.norm(v2) > 0 else v2
        v3 = v3 / np.linalg.norm(v3) if np.linalg.norm(v3) > 0 else v3
        
        return np.array([v1, v2, v3])
    
    def apply_to_point(self, point: np.ndarray) -> np.ndarray:
        """Apply transformation to a point"""
        if self.is_displacement:
            # Displacement: translate then rotate
            return self.rotation @ point + self.translation
        else:
            # Standard: translate then rotate
            return self.rotation @ (point - self.translation)
    
    def apply_to_vector(self, vector: np.ndarray) -> np.ndarray:
        """Apply rotation to a vector (no translation)"""
        return self.rotation @ vector
    
    def inverse(self) -> 'TransformationMatrix':
        """Get inverse transformation"""
        inv = TransformationMatrix(self.tr_number)
        inv.rotation = self.rotation.T
        inv.translation = -inv.rotation @ self.translation
        inv.is_displacement = not self.is_displacement
        return inv
    
    def to_homogeneous(self) -> np.ndarray:
        """Convert to 4x4 homogeneous transformation matrix"""
        mat = np.eye(4)
        mat[0:3, 0:3] = self.rotation
        mat[0:3, 3] = self.translation
        return mat
    
    def to_tr_card(self) -> str:
        """Convert back to TR card format"""
        params = list(self.translation)
        params.extend(self.rotation[0, :])
        params.extend(self.rotation[1, :])
        params.extend(self.rotation[2, :])
        if self.is_displacement:
            params.append(1)
        
        card = f"tr{self.tr_number}"
        for p in params:
            card += f" {p:.6f}"
        return card


def apply_transformation(point: Tuple[float, float, float], 
                        tr_card: List[float], 
                        is_degrees: bool = False) -> Tuple[float, float, float]:
    """
    Apply MCNP transformation to a point
    
    Args:
        point: (x, y, z) coordinates
        tr_card: TR card parameters
        is_degrees: True for *TR (degrees), False for TR (direction cosines)
    
    Returns:
        Transformed (x, y, z) coordinates
    """
    trans = TransformationMatrix.from_tr_card(tr_card, is_degrees)
    point_array = np.array(point)
    result = trans.apply_to_point(point_array)
    return tuple(result)


def compose_transformations(tr1: TransformationMatrix, tr2: TransformationMatrix) -> TransformationMatrix:
    """
    Compose two transformations: apply tr1 then tr2
    
    Returns:
        Combined transformation
    """
    result = TransformationMatrix()
    
    # Compose rotation matrices
    result.rotation = tr2.rotation @ tr1.rotation
    
    # Compose translations
    result.translation = tr2.rotation @ tr1.translation + tr2.translation
    
    return result


def rotation_matrix_x(angle_deg: float) -> np.ndarray:
    """Rotation matrix around X axis"""
    angle_rad = np.radians(angle_deg)
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ])


def rotation_matrix_y(angle_deg: float) -> np.ndarray:
    """Rotation matrix around Y axis"""
    angle_rad = np.radians(angle_deg)
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    return np.array([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ])


def rotation_matrix_z(angle_deg: float) -> np.ndarray:
    """Rotation matrix around Z axis"""
    angle_rad = np.radians(angle_deg)
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])


def euler_to_rotation(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """
    Convert Euler angles (degrees) to rotation matrix
    
    Args:
        roll: Rotation around X axis
        pitch: Rotation around Y axis
        yaw: Rotation around Z axis
    
    Returns:
        3x3 rotation matrix
    """
    return rotation_matrix_z(yaw) @ rotation_matrix_y(pitch) @ rotation_matrix_x(roll)


if __name__ == "__main__":
    # Test transformations
    tr = TransformationMatrix.from_tr_card([10, 20, 30, 1, 0, 0, 0, 1, 0, 0, 0, 1])
    point = np.array([0, 0, 0])
    result = tr.apply_to_point(point)
    print(f"Transformed point: {result}")
    print(f"TR card: {tr.to_tr_card()}")

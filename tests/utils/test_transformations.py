"""
Test suite for utils/transformations.py
"""
import pytest
import numpy as np
from utils.transformations import TransformationMatrix, apply_transformation, rotation_matrix_z

class TestTransformations:
    
    def test_identity_transformation(self):
        """Test identity transformation"""
        tm = TransformationMatrix()
        point = np.array([1.0, 2.0, 3.0])
        result = tm.apply_to_point(point)
        
        np.testing.assert_array_almost_equal(result, point)
    
    def test_translation(self):
        """Test pure translation"""
        tm = TransformationMatrix(translation=[5.0, 0.0, 0.0])
        point = np.array([1.0, 2.0, 3.0])
        result = tm.apply_to_point(point)
        
        expected = np.array([6.0, 2.0, 3.0])
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_rotation_z_90deg(self):
        """Test 90-degree rotation about Z axis"""
        rot_mat = rotation_matrix_z(90)
        tm = TransformationMatrix(rotation=rot_mat)
        
        point = np.array([1.0, 0.0, 0.0])
        result = tm.apply_to_point(point)
        
        expected = np.array([0.0, 1.0, 0.0])
        np.testing.assert_array_almost_equal(result, expected, decimal=5)
    
    def test_combined_transformation(self):
        """Test rotation + translation"""
        rot_mat = rotation_matrix_z(90)
        tm = TransformationMatrix(
            rotation=rot_mat,
            translation=[1.0, 0.0, 0.0]
        )
        
        point = np.array([1.0, 0.0, 0.0])
        result = tm.apply_to_point(point)
        
        # Rotates [1,0,0] to [0,1,0], then translates by [1,0,0] to [1,1,0]
        expected = np.array([1.0, 1.0, 0.0])
        np.testing.assert_array_almost_equal(result, expected, decimal=5)
    
    def test_parse_tr_card(self):
        """Test parsing TR card"""
        tr_string = "tr1  1.0 2.0 3.0  90 90 0  1"
        # This would need the actual parser implementation
        # Placeholder for testing TR card parsing
        pass

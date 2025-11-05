#!/usr/bin/env python3
"""
MCNP Transformation Calculator

Calculates TR card values from Euler angles, rotation matrices,
or combined transformations.

Usage:
    python transformation_calculator.py --euler 30 45 60
    python transformation_calculator.py --translate 10 0 0
    python transformation_calculator.py --euler 0 30 0 --translate 5 0 0

Output:
    MCNP-formatted *TR card
"""

import numpy as np
import argparse

def euler_to_rotation_matrix(roll_x, pitch_y, yaw_z, degrees=True):
    """
    Convert Euler angles to rotation matrix.

    Parameters:
        roll_x: Rotation about x-axis
        pitch_y: Rotation about y-axis
        yaw_z: Rotation about z-axis
        degrees: If True, angles in degrees; else radians

    Returns:
        3x3 rotation matrix
    """
    if degrees:
        roll_x = np.radians(roll_x)
        pitch_y = np.radians(pitch_y)
        yaw_z = np.radians(yaw_z)

    # Rotation matrices
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(roll_x), -np.sin(roll_x)],
                   [0, np.sin(roll_x), np.cos(roll_x)]])

    Ry = np.array([[np.cos(pitch_y), 0, np.sin(pitch_y)],
                   [0, 1, 0],
                   [-np.sin(pitch_y), 0, np.cos(pitch_y)]])

    Rz = np.array([[np.cos(yaw_z), -np.sin(yaw_z), 0],
                   [np.sin(yaw_z), np.cos(yaw_z), 0],
                   [0, 0, 1]])

    # Combined: Rz * Ry * Rx (MCNP convention)
    return Rz @ Ry @ Rx

def rotation_matrix_to_euler(R):
    """
    Convert rotation matrix to Euler angles.

    Parameters:
        R: 3x3 rotation matrix

    Returns:
        (roll_x, pitch_y, yaw_z) in degrees
    """
    pitch_y = np.arcsin(-R[2, 0])

    if np.cos(pitch_y) != 0:
        roll_x = np.arctan2(R[2, 1], R[2, 2])
        yaw_z = np.arctan2(R[1, 0], R[0, 0])
    else:
        # Gimbal lock
        roll_x = 0
        yaw_z = np.arctan2(-R[0, 1], R[1, 1])

    return (np.degrees(roll_x), np.degrees(pitch_y), np.degrees(yaw_z))

def verify_rotation_matrix(R, tol=1e-6):
    """
    Verify rotation matrix is orthonormal with det=+1.

    Returns:
        (is_valid, message)
    """
    # Check orthonormality: R * R.T should be identity
    identity_check = R @ R.T
    if not np.allclose(identity_check, np.eye(3), atol=tol):
        return (False, "Matrix is not orthonormal (R*R.T != I)")

    # Check determinant is +1
    det = np.linalg.det(R)
    if not np.isclose(det, 1.0, atol=tol):
        if np.isclose(det, -1.0, atol=tol):
            return (False, f"Determinant = -1 (reflection, not rotation)")
        else:
            return (False, f"Determinant = {det:.6f} (should be +1)")

    return (True, "Valid rotation matrix")

def format_tr_card(tr_num, translation, rotation_matrix=None, use_degrees=True):
    """
    Format MCNP *TR card.

    Parameters:
        tr_num: Transformation number
        translation: (dx, dy, dz) tuple
        rotation_matrix: 3x3 matrix (optional, identity if None)
        use_degrees: If True and rotation is simple, use degree format

    Returns:
        Formatted *TR card string
    """
    dx, dy, dz = translation

    if rotation_matrix is None:
        # Translation only
        return f"*TR{tr_num}  {dx} {dy} {dz}"

    # Check if rotation is identity (no rotation)
    if np.allclose(rotation_matrix, np.eye(3)):
        return f"*TR{tr_num}  {dx} {dy} {dz}"

    # Try to express as Euler angles if use_degrees
    if use_degrees:
        try:
            euler = rotation_matrix_to_euler(rotation_matrix)
            roll, pitch, yaw = euler

            # Check if single-axis rotation (simpler)
            if np.isclose(roll, 0) and np.isclose(yaw, 0):
                # Rotation about y-axis only
                return f"*TR{tr_num}  {dx} {dy} {dz}  0 {pitch:.3f} 0  1"
            elif np.isclose(pitch, 0) and np.isclose(yaw, 0):
                # Rotation about x-axis only
                return f"*TR{tr_num}  {dx} {dy} {dz}  {roll:.3f} 0 0  1"
            elif np.isclose(roll, 0) and np.isclose(pitch, 0):
                # Rotation about z-axis only
                return f"*TR{tr_num}  {dx} {dy} {dz}  0 0 {yaw:.3f}  1"
            else:
                # General Euler angles
                return f"*TR{tr_num}  {dx} {dy} {dz}  {roll:.3f} {pitch:.3f} {yaw:.3f}  1"
        except:
            pass  # Fall through to matrix format

    # Full matrix format
    R = rotation_matrix
    card = f"*TR{tr_num}  {dx} {dy} {dz}  "
    card += f"{R[0,0]:.6f} {R[0,1]:.6f} {R[0,2]:.6f}  "
    card += f"{R[1,0]:.6f} {R[1,1]:.6f} {R[1,2]:.6f}  "
    card += f"{R[2,0]:.6f} {R[2,1]:.6f} {R[2,2]:.6f}"

    return card

def main():
    parser = argparse.ArgumentParser(description='MCNP Transformation Calculator')
    parser.add_argument('--tr', type=int, default=1, help='TR number (default: 1)')
    parser.add_argument('--translate', nargs=3, type=float, metavar=('DX', 'DY', 'DZ'),
                       help='Translation vector (dx dy dz)', default=[0, 0, 0])
    parser.add_argument('--euler', nargs=3, type=float, metavar=('RX', 'RY', 'RZ'),
                       help='Euler angles in degrees (roll pitch yaw)')
    parser.add_argument('--rotate-x', type=float, metavar='ANGLE',
                       help='Rotation about x-axis (degrees)')
    parser.add_argument('--rotate-y', type=float, metavar='ANGLE',
                       help='Rotation about y-axis (degrees)')
    parser.add_argument('--rotate-z', type=float, metavar='ANGLE',
                       help='Rotation about z-axis (degrees)')
    parser.add_argument('--verify', action='store_true',
                       help='Verify rotation matrix validity')

    args = parser.parse_args()

    translation = tuple(args.translate)

    # Determine rotation
    rotation_matrix = None

    if args.euler:
        roll, pitch, yaw = args.euler
        rotation_matrix = euler_to_rotation_matrix(roll, pitch, yaw)
        print(f"Euler angles: Roll={roll}°, Pitch={pitch}°, Yaw={yaw}°")
    elif args.rotate_x:
        rotation_matrix = euler_to_rotation_matrix(args.rotate_x, 0, 0)
        print(f"Rotation: {args.rotate_x}° about x-axis")
    elif args.rotate_y:
        rotation_matrix = euler_to_rotation_matrix(0, args.rotate_y, 0)
        print(f"Rotation: {args.rotate_y}° about y-axis")
    elif args.rotate_z:
        rotation_matrix = euler_to_rotation_matrix(0, 0, args.rotate_z)
        print(f"Rotation: {args.rotate_z}° about z-axis")

    if translation != (0, 0, 0):
        print(f"Translation: dx={translation[0]}, dy={translation[1]}, dz={translation[2]}")

    # Verify rotation matrix if requested
    if rotation_matrix is not None and args.verify:
        print("\n" + "=" * 60)
        print("ROTATION MATRIX VERIFICATION")
        print("=" * 60)
        print("\nRotation Matrix:")
        print(rotation_matrix)
        print(f"\nDeterminant: {np.linalg.det(rotation_matrix):.6f}")

        is_valid, message = verify_rotation_matrix(rotation_matrix)
        print(f"Validity: {message}")

        if not is_valid:
            print("\n⚠️  WARNING: Matrix is not a valid rotation matrix!")
            return

    # Generate TR card
    print("\n" + "=" * 60)
    print("MCNP TR CARD")
    print("=" * 60)
    tr_card = format_tr_card(args.tr, translation, rotation_matrix)
    print(f"\n{tr_card}\n")

    # Additional info
    if rotation_matrix is not None:
        print("Full Matrix Representation:")
        print(f"*TR{args.tr}  {translation[0]} {translation[1]} {translation[2]}  \\")
        R = rotation_matrix
        print(f"       {R[0,0]:.6f} {R[0,1]:.6f} {R[0,2]:.6f}  \\")
        print(f"       {R[1,0]:.6f} {R[1,1]:.6f} {R[1,2]:.6f}  \\")
        print(f"       {R[2,0]:.6f} {R[2,1]:.6f} {R[2,2]:.6f}")

if __name__ == '__main__':
    main()

import numpy as np

class Vector3(np.ndarray):  
    """
    A 3D vector.
    """
    def __new__(cls, value=None, dtype=None):
        return np.array(value, dtype=dtype).view(Vector3)


def from_matrix44_translation(mat, dtype=None):
    """
    Create a Vector3 from a Matrix44.
    """
    return np.array(mat[3, :3], dtype=dtype)

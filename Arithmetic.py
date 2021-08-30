import numpy as np


def multiply(m1, m2):
    """Multiply two matricies, m1 . m2.
    """
    return np.dot(m1, m2)

    
def create_identity(dtype=None):
    """Creates a new matrix44 and sets it to an identity matrix with shape (4,4).
    """
    return np.identity(4, dtype=dtype)


def create_from_scale(scale, dtype=None):
    """Creates an identity matrix with (4,4) the scale set.
     we need to expand 'scale' into it's components because numpy isn't flattening them properly.
    """
    m = np.diagflat([scale[0], scale[1], scale[2], 1.0])
    if dtype:
        m = m.astype(dtype)
    return m

def create_from_translation(vec, dtype=None):
    """Creates an identity matrix with the translation set.
    :param numpy.array vec: The translation vector (shape 3 or 4).
    :return: numpy.array ; A matrix with shape (4,4) that represents a matrix
            with the translation set to the specified vector.
    """
    dtype = dtype or vec.dtype
    mat = create_identity(dtype)
    mat[3, 0:3] = vec[:3]
    return mat

def create_from_y_rotation(theta, dtype=None):
    """Creates a matrix with the specified rotation about the Y axis.
    :return: A matrix with the shape (4,4) with the specified rotation about the Y-axis.
    """
    cosT = np.cos(theta)
    sinT = np.sin(theta)
    mat = create_identity(dtype)

    mat[0:3, 0:3] = np.array(
        [
            [ cosT, 0.0,sinT ],
            [ 0.0, 1.0, 0.0 ],
            [-sinT, 0.0, cosT ]
        ],
        dtype=dtype
    )

    return mat


def create_from_z_rotation(theta, dtype=None):
    """Creates a matrix with the specified rotation about the Z axis.
    :return: A matrix with the shape (4,4) with the specified rotation about the Z-axis.
    """
    cosT = np.cos(theta)
    sinT = np.sin(theta)
    mat = create_identity(dtype)

    mat[0:3, 0:3] = np.array(
        [
            [ cosT,-sinT, 0.0 ],
            [ sinT, cosT, 0.0 ],
            [ 0.0, 0.0, 1.0 ]
        ],
        dtype=dtype
    )

    return mat


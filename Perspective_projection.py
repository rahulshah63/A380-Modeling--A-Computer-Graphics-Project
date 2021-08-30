import numpy as np

def create_perspective_projection(fovy, aspect, near, far, dtype=None):
    """
    :param float fovy: field of view in y direction in degrees
    :param float aspect: aspect ratio of the view (width / height)
    :param float near: distance from the viewer to the near clipping plane (only positive)
    :param float far: distance from the viewer to the far clipping plane (only positive)

    :return: A projection matrix representing the specified perpective.
    
            /|
           / | (ymax)
          /  |
         /   |
        /    |
    cam/_____|
         near

    """
    ymax = near * np.tan(fovy * np.pi / 360.0)
    xmax = ymax * aspect
    return create_perspective_projection_from_bounds(-xmax, xmax, -ymax, ymax, near, far, dtype=dtype)

def create_perspective_projection_from_bounds(
    left,
    right,
    bottom,
    top,
    near,
    far,
    dtype=None
):
    """Creates a perspective projection matrix using the specified near plane dimensions.

    left: The left of the near plane relative to the plane's centre.
    right: The right of the near plane relative to the plane's centre.
    top: The top of the near plane relative to the plane's centre.
    bottom: The bottom of the near plane relative to the plane's centre.
    near: The distance of the near plane from the camera's origin.
    far: The distance of the far plane from the camera's origin.

    :return: A projection matrix representing the specified perspective.
    """

    A = (right + left) / (right - left)
    B = (top + bottom) / (top - bottom)
    C = -(far + near) / (far - near)
    D = -2. * far * near / (far - near)
    E = 2. * near / (right - left)
    F = 2. * near / (top - bottom)

    return np.array((
        (  E, 0., 0., 0.),
        ( 0.,  F, 0., 0.),
        (  A,  B,  C,-1.),
        ( 0., 0.,  D, 0.),
    ), dtype=dtype)

import numpy as np

def normalize(vec):
    """normalizes an Nd list of vectors or a single vector
    to unit length.
    """

    return (vec / np.sqrt(np.sum(vec**2, axis=-1)))


def create_look_at(eye, target, up, dtype=None):
    """
    :param numpy.array eye: Position of the camera in world coordinates.
    :param numpy.array target: The position in world coordinates that the camera is looking at.
    :param numpy.array up: The up vector of the camera.

    :return: A look at matrix that can be used as a viewMatrix
    """

    eye = np.asarray(eye)
    target = np.asarray(target)
    up = np.asarray(up)

    # computes the forward vector from camera to the target
    forward = normalize(eye - target) #make unit length
    side = normalize(np.cross(forward, up)) #compute the side(left) vector
    up = (np.cross(side, forward)) #recompute the orthonormal up vector

    return np.array((
            #set rotation part and translation part
            (side[0], up[0], forward[0], 0.),
            (side[1], up[1], forward[1], 0.),
            (side[2], up[2], forward[2], 0.),
            (-np.dot(side, eye), -np.dot(up, eye), -np.dot(forward, eye), 1.0)
        ), dtype=dtype)


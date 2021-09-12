import numpy as np

def normalized(vector):
    len = np.linalg.norm(vector)
    if np.isclose(len, 0):
        return np.array([0, 0])
    return vector / len
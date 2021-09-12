import numpy as np

class Vector2:
    # Constructors
    def __init__(self):
        self.x = 0. # instance variables
        self.y = 0.
    
    def __init__(self, x, y): # the first parameter (usually called self) is used to access to instance variables
        self.x = x
        self.y = y
    
    # Overload operators
    def __add__(v1, v2):
        return Vector2(v1.x + v2.x, v1.y + v2.y)
    
    def __IADD__(self, other):
        self = self + other
    
    def __sub__(v1, v2):
        return Vector2(v1.x - v2.x, v1.y - v2.y)
    
    def __ISUB__(self, other):
        self = self - other

    def __mul__(c, v):
        return Vector2(c * v.x, c * v.y)
    
    def __mul__(v, c):
        return Vector2(c * v.x, c * v.y)
    
    def __truediv__(v, c):
        return Vector2(v.x / c, v.y / c)
    
    # Methods
    def zero():
        return Vector2()
    
    def ones():
        return Vector2(1., 1.)

    def magnitude(v):
        return np.sqrt(np.power(v.x, 2.) + np.power(v.y, 2.))

    def normalized(v):
        len = v.magnitude
        if np.isclose(len, 0):
            return Vector2.zero()
        return v / len

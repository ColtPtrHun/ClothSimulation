import numpy as np

class Vector2:
    # Constructor
    def __init__(self, x=0, y=0):
        # The first parameter (usually called self) is used to access to instance variables
        # There are no function overloads. There are optional arguments instead.
        self.x, self.y = x, y # instance variables
    
    # Overload operators
    def __add__(v1, v2):
        return Vector2(v1.x + v2.x, v1.y + v2.y)
    def __IADD__(self, other):
        self = self + other
    
    def __sub__(v1, v2):
        return Vector2(v1.x - v2.x, v1.y - v2.y)
    def __ISUB__(self, other):
        self = self - other

    #def __mul__(c, v):
        #return Vector2(c * v.x, c * v.y)
    def __mul__(v, c):
        return Vector2(c * v.x, c * v.y)
    def __IMUL__(self, c):
        self = c * self
    
    def __truediv__(v, c):
        return Vector2(v.x / c, v.y / c)
    def __IDIV__(self, c):
        self = self / c
    
    # Methods
    def print(self, name='v'):
        print(name + ' = ({:.2f}'.format(self.x) + ', {:.2f}'.format(self.y) + ')')

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

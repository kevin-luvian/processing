from math import sqrt, cos, sin, radians

def add_vect(vect_a, vect_b):
    return [vect_a[0] + vect_b[0], vect_a[1] + vect_b[1]]
        
def sub_vect(vect_a, vect_b):
    return [vect_a[0] - vect_b[0], vect_a[1] - vect_b[1]]

def mult_vect(vect, scalar):
    return [vect.x * scalar, vect.y * scalar]

def dot_vect(v_a, v_b):
    return (v_a[0] * v_b[0]) + (v_a[1] * v_b[1])

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        else:
            return NotImplemented
    
    def __str__(self):
        return "Vector(x: {0:.2f} y: {1:.2f})".format(self.x, self.y)
        
    def rotate(self, deg):
        deg = radians(deg)
        temp_x = self.x * cos(deg) + self.y * -sin(deg)
        temp_y = self.x * sin(deg) + self.y * cos(deg)
        self.x = 0 if abs(temp_x) <= 0.001 else temp_x
        self.y = 0 if abs(temp_y) <= 0.001 else temp_y
        return self
    
    def add(self, v):
        self.x += v.x
        self.y += v.y
        return self
    
    def sub(self, v):
        self.x -= v.x
        self.y -= v.y
        return self
    
    def mult(self, scalar):
        self.x *= scalar
        self.y *= scalar
        return self
    
    def project(self, v):
        mul = self.dot(v) / v.dot(v)
        p = mult_vect(v, mul)
        self.x = p[0]
        self.y = p[1]
        return self
    
    def normalize(self):
        l = self.length()
        if l == 0:
            self.x = 0
            self.y = 0
        else:
            self.mult(1 / l)
        return self
        
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def project_scalar(self, v):
        try:
            return self.dot(v) / v.length()
        except ZeroDivisionError:
            return 0
        
    def dot(self, v):
        return (self.x * v.x) + (self.y * v.y)
    
    def copy(self):
        return Vector(self.x, self.y)
        
    def get_val(self):
        return [self.x, self.y]

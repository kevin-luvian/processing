from vector2d import Vector
import unittest

class TestVector2d(unittest.TestCase):        
    def test_dot_product(self):
        v_a = Vector(1,2)
        v_p = Vector(3,4)
        d = v_a.dot(v_p)
        self.assertEqual(d, 11)
        
    def test_length(self):
        v_a = Vector(3,4)
        l = v_a.length()
        self.assertEqual(l,5)
        
    def test_add_and_mult(self):
        v_a = Vector(3,4)
        v_b = Vector(1,1)
        v_a.add(v_b)
        self.assertEqual(v_a, Vector(4,5))
        
        v_a = Vector(3,4)
        v_a.mult(5)
        self.assertEqual(v_a, Vector(15,20))
        
    def test_vector_projection(self):
        v_a = Vector(3, 4)
        v_p = Vector(-1, 0)
        v_a.project(v_p)
        self.assertEqual(v_a, Vector(3, 0))
        
        v_a = Vector(1, 2)
        v_p = Vector(3, 4)
        v_a.project(v_p)
        self.assertEqual(v_a, Vector(1.32, 1.76))
        
    def test_scalar_projection(self):
        v_a = Vector(1,2)
        v_p = Vector(3,4)
        scal = v_a.project_scalar(v_p)
        self.assertEqual(scal, 2.2)
        
    def test_rotation(self):
        v_a = Vector(0,1)
        v_a.rotate(-90)
        self.assertEqual(v_a, Vector(1,0))
        
        v_a = Vector(1,1)
        v_a_len = v_a.length()
        v_a.rotate(-45)
        self.assertEqual(int(v_a.x), int(v_a_len))
        self.assertEqual(v_a.y, 0)

if __name__ == '__main__':
    unittest.main()

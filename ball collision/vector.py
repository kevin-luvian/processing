
def mult_vect(vect, mult):
    return [vect[0] * mult, vect[1] * mult]

def add_vect(vect_a, vect_b):
    return [vect_a[0] + vect_b[0], vect_a[1] + vect_b[1]]

def sub_vect(vect_a, vect_b):
    return [vect_a[0] - vect_b[0], vect_a[1] - vect_b[1]]

def normalize_vect(vect):
    length = sqrt(vect[0] ** 2 + vect[1] ** 2)
    if length == 0:
        return [0, 0]
    return mult_vect(vect, 1 / length)

def length_vect(vect):
    return  sqrt(vect[0] ** 2 + vect[1] ** 2)

def limit_vect(vect, lim):
    if length_vect(vect) > lim:
        return max_vect(vect, lim)
    return vect

def max_vect(vect, max_val):
    return mult_vect(normalize_vect(vect), max_val)

def distance_pos(pos_a, pos_b):
    comb_pos = sub_vect(pos_a, pos_b)
    return sqrt(comb_pos[0] ** 2 + comb_pos[1] ** 2)

def rotate_vect(vect, degree):
    x = vect[0] * cos(degree) - vect[1] * sin(degree)
    y = vect[0] * sin(degree) + vect[1] * cos(degree)
    return [x, y]

def degree_between_vect(vect_a, vect_b):
    return degrees(acos(dot_vect(vect_a, vect_b)/(length_vect(vect_a)*length_vect(vect_b))))
    
def dot_vect(vect_a, vect_b):
    return (vect_a[0] * vect_b[0]) + (vect_a[1] * vect_b[1])
    
def proj_vect(vect_a, vect_b):
    return mult_vect(vect_b, proj_scalar(vect_a, vect_b))

def proj_scalar(vect_a, vect_b):
    try:
        return dot_vect(vect_a, vect_b) / (length_vect(vect_b) ** 2)
    except ZeroDivisionError:
        return 0

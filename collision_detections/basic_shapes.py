from vector2d import Vector, sub_vect, add_vect, dot_vect
from collections import namedtuple

Collision = namedtuple('Collision', ['is_collide', 'v'])

class SPoly:    
    def __init__(self, pos_x, pos_y, r, np):
        self.points = []
        self.line_color = (100, 100, 100)
        self.is_collide = False
        
        self.acc = Vector(0, 0)
        self.vel = Vector(0, 0)
        self.pos = Vector(pos_x, pos_y)
        
        self.r = r
        self.np = np
        self.create_points()
        
    def create_points(self):
        v_len = Vector(self.r, 0).rotate(-90)
        deg = 360 / self.np
        
        for i in range(0, self.np):
            self.points.append([v_len.x, v_len.y])
            v_len.rotate(deg)
    
    def update(self):
        self.draw_rays()
                
        # self.check_mouse()
        self.update_avp()
        
        if self.is_collide:
            self.line_color = (255, 0, 0)
        else:
            self.line_color = (100, 100, 100)
        self.is_collide = False
        
    def attract_to(self, p_x, p_y):
        v = Vector(p_x, p_y).sub(self.pos).normalize().mult(.5)
        self.acc.add(v)
        
    def update_avp(self):
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc.mult(0)
        self.displace_from_window()
        
    def displace_from_window(self):
        rays = self.get_point_rays()
        for p, r in zip(self.points, rays):
            p = (p[0] + self.pos.x, p[1] + self.pos.y)
            if r[0] <= 0 or r[0] >= width:
                v_x_dis = (p[0] - r[0], 0)
                self.acc.add(Vector(*v_x_dis))
                if r[0] <= 0:
                    self.pos.x -= p[0]
                else:
                    self.pos.x += width - p[0]
            if r[1] <= 0 or r[1] >= height:
                v_x_dis = (0, p[1] - r[1])
                self.acc.add(Vector(*v_x_dis))
                if r[1] <= 0:
                    self.pos.y -= p[1]
                else:
                    self.pos.y += height - p[1]
        
    def draw_rays(self):
        stroke(255, 255, 0)
        rays = self.get_point_rays()
        for p, r in zip(self.points, rays):
            line(self.pos.x+p[0], self.pos.y+p[1], r[0], r[1])
        
    def get_point_rays(self):
        rays = []
        for p in self.points:
            p = (self.pos.x + p[0], self.pos.y + p[1])
            rays.append((p[0] + self.vel.x, p[1]+self.vel.y))
        return rays
    
    def get_current_points(self):
        points = []
        for p in self.points:
            points.append((self.pos.x + p[0], self.pos.y + p[1]))
        return points
            
    def check_for_collisions(self, objs):
        self.is_collide = False
        for obj in objs:
            if obj is self:
                continue
            print("checking collision")
            print("vel",str(self.vel))
            s_col = self.check_collision(obj)
            if s_col.is_collide:
                print("displacement n:", self.np,"v: ", str(s_col.v))
                s_col.v.mult(-1)
                # s_col.v.add(self.pos)
                # stroke(255)
                # line(self.x, self.y, self.x+s_col.v.x, self.y+s_col.v.y)
                o_col = obj.check_collision(self)
                if o_col.is_collide:
                    self.is_collide = True
                    d_v = s_col.v
                    if o_col.v.length() < s_col.v.length():
                        d_v = o_col.v
                    d_v = self.calc_displace_direction(obj, d_v)
                    # self.vel.mult(0)
                    self.acc.add(d_v)
                    
                    stroke(255)
                    line(self.pos.x, self.pos.y, d_v.x + self.pos.x, d_v.y + self.pos.y)
    
    def calc_displace_direction(self, poly, d_v):
        if self.pos.x < poly.pos.x:
            d_v.x = -abs(d_v.x)
        else:
            d_v.x = abs(d_v.x)
        if self.pos.y < poly.pos.y:
            d_v.y = -abs(d_v.y)
        else:
            d_v.y = abs(d_v.y)
        return d_v
    
    def check_collision(self, poly):
        l_p = len(self.points)
        displacement = [0, 0]
        min_dis = None
        for n in range(l_p):
            if n + 1 < l_p:
                axes = sub_vect(self.points[n], self.points[n + 1])
            else:
                axes = sub_vect(self.points[n], self.points[0])
            axes_normal = Vector(*axes).rotate(90).normalize()
            s_p = self.axes_projections(axes_normal, self.get_current_points())
            p_p = poly.axes_projections(axes_normal, poly.get_current_points())
            if s_p[0] >= p_p[1] or s_p[1] <= p_p[0]:
                return Collision(False, displacement)
            new_dis = self.find_dis_len(s_p, p_p)
            if min_dis is None or abs(new_dis) < min_dis:
                min_dis = abs(new_dis)
                displacement = axes_normal.mult(min_dis)
        print("min_dis", min_dis)
        return Collision(True, displacement)
    
    def find_dis_len(self, l_1, l_2):
        if l_1[0] < l_2[0]:
            if l_1[1] < l_2[1]:
                return l_1[1] - l_2[0]
            return l_2[1] - l_2[0]
        if l_1[0] > l_2[0]:
            return l_2[1] - l_1[0]
        return l_1[1] - l_1[0]
    
    def axes_projections(self, axes_normal, points):
        n_min = dot_vect(points[0], axes_normal.get_val())
        n_max = n_min
        for i in range(1, len(points)):
            p_scal = dot_vect(points[i], axes_normal.get_val())
            if p_scal < n_min:
                n_min = p_scal
            elif p_scal > n_max:
                n_max = p_scal
        return (n_min, n_max)
    
    def intersected_axes(self, poly):
        pass
            
    def check_mouse(self):
        c = self.contains_point(mouseX, mouseY)
        ellipse(mouseX, mouseY, 5, 5)
        if c:
            self.is_collide = True
    
    def contains_point(self, p_x, p_y):
        l_p = len(self.points)
        for n in range(l_p):
            if n + 1 < l_p:
                axes = sub_vect(self.points[n], self.points[n + 1])
            else:
                axes = sub_vect(self.points[n], self.points[0])
            axes_normal = Vector(*axes).rotate(90).normalize()
            s_p = self.axes_projections(axes_normal)
            p_scal = dot_vect([p_x, p_y], axes_normal.get_val())
            if s_p[0] >= p_scal or s_p[1] <= p_scal:
                return False
        return True
        
    def draw(self):
        if len(self.points) == 0:
            return
        # stroke(*self.line_color)
        s = createShape()
        s.beginShape()
        s.noFill()
        s.stroke(*self.line_color)
        for p in self.points:
            p_x = self.pos.x + p[0]
            p_y = self.pos.y + p[1]
            s.vertex(p_x, p_y)
            # line(self.x, self.y, p_x, p_y)
        s.vertex(self.pos.x + self.points[0][0], self.pos.y + self.points[0][1])
        s.endShape()
        shape(s)

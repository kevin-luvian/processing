import vector
from random import randint

# max_vel = 1
acc_mult = 1

class Ball:
    is_colliding = False
    collision_counter = 0
    acc = [0,0]
    vel = [0,0]
    
    def __init__(self, x, y, radius):
        self.pos = [x,y]
        # track current pos for displacement
        self.current_pos = [x,y]
        self.radius = radius
        self.mass = radius * 1.0
        # self.vel = [randint(-10,10), randint(-10,10)]
        
    def set_heading(self, heading_pos, heading_vel):
        vect_heading = vector.sub_vect(heading_pos, self.pos)
        vect_heading = vector.max_vect(vect_heading, heading_vel)
        # vect_heading = vector.sub_vect(vect_heading, self.vel)
        self.vel = vect_heading
        
    def update(self):
        self.collide_window()
        # self.acc = vector.mult_vect(self.acc, acc_mult)
        self.vel = vector.add_vect(self.vel, self.acc)
        self.pos = vector.add_vect(self.pos, self.vel)
        self.acc = [0, 0]
        # self.dampen()
        self.current_pos = self.pos
        
    def dampen(self):
        if vector.length_vect(self.vel) < 0.01:
            self.vel = [0,0]
        else:
            opposing_vel = vector.mult_vect(vector.normalize_vect(self.vel), -.005)
            self.vel = vector.add_vect(self.vel, opposing_vel)
        
    def collide(self, ball):
        dist_x =  ball.current_pos[0] - self.current_pos[0]
        dist_y =  ball.current_pos[1] - self.current_pos[1]
        overlap = self.radius + ball.radius - sqrt(dist_x ** 2 + dist_y ** 2)
        if overlap >= 0 :
            self.is_colliding = True
            # print("dist_x", dist_x, "dist_y", dist_y, "distance", sqrt(dist_x ** 2 + dist_y ** 2),"overlap", overlap)
            coll_normal = vector.normalize_vect([-dist_x, -dist_y])
            # self.equal_mass_collision(coll_normal, ball)
            self.different_mass_collision(coll_normal, ball)
        
            if overlap > 0:
                self.displace_pos(coll_normal, overlap)
                
        # if dist_x < 0:
        stroke(255, 0, 0, 100)
        line(self.pos[0], self.pos[1], ball.pos[0], ball.pos[1])
            # noFill()
            # ellipse(self.current_pos[0], self.current_pos[1], 30 * 2, 30 * 2)
        
    def equal_mass_collision(self, coll_normal, ball):
        comb_vel = vector.sub_vect(ball.vel, self.vel)
        total_proj = vector.proj_vect(comb_vel, coll_normal)
        self.acc = vector.add_vect(self.acc, total_proj)
        
    def different_mass_collision(self, coll_normal, ball):
        vect_1 = vector.mult_vect(self.vel, ((self.mass - ball.mass) / (self.mass + ball.mass)))
        vect_2 = vector.mult_vect(ball.vel, ((ball.mass * 2) / (self.mass + ball.mass)))
        vect_total = vector.add_vect(vect_1, vect_2)
        # force = vector.proj_vect(vector.sub_vect(vect_total, self.vel), coll_normal)
        force = vector.proj_vect(vector.sub_vect(vect_total, self.vel), coll_normal)
        # print("self mass",self.mass," vel", self.vel, "sep vect", vect_total, "sep force", force, "sep vel", vector.add_vect(self.vel, force))
        self.acc = vector.add_vect(self.acc, force)
        
    def displace_pos(self, coll_normal, overlap):
        displacement_vect = vector.mult_vect(coll_normal, overlap*.5)
        self.pos = vector.add_vect(self.pos, displacement_vect)
            
    def collide_window(self):
        if self.pos[0] + self.radius >= width or self.pos[0] - self.radius <= 0:
            self.vel[0] = -self.vel[0]
            if self.pos[0] + self.radius > width:
                self.pos[0] = width - self.radius
            elif self.pos[0] - self.radius < 0:
                self.pos[0] = self.radius
        if self.pos[1] + self.radius >= height or self.pos[1] - self.radius <= 0:
            self.vel[1] = -self.vel[1]
            if self.pos[1] + self.radius > height:
                self.pos[1] = height - self.radius
            elif self.pos[1] - self.radius < 0:
                self.pos[1] = self.radius
    
    def show(self):
        noStroke()
        if self.is_colliding:
            # fill(255, 255, 255)
            fill(255, 0, 0, 190)
            # ellipse(self.pos[0], self.pos[1], self.radius * 2, self.radius * 2)
            if self.collision_counter % 5 == 0:
                self.is_colliding = False
            self.collision_counter += 1
        else:
            fill(255, 0, 0, 100)
            # fill(255)
        ellipse(self.pos[0], self.pos[1], self.radius * 2, self.radius * 2)
        pass

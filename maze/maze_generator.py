import collections as col
import random 

Block = col.namedtuple('Block', ['pos','dir'])
Pos = col.namedtuple('Pos', ['x','y'])
No = 0
Left = 1
Top = 2
Right = 3
Bottom = 4
   
def genl(val):
    return lambda n:[val for i in range(n)]

class Generator:
    def __init__(self, win_w, win_h, x_n, y_n):
        self.finished = False
        self.w = x_n
        self.h = y_n
        self.x_len = (win_w - .5)/self.w
        self.y_len = (win_h - .5)/self.h
        
        self.flags = [[False for i in range(x_n)] for j in range(y_n)]
        self.nodes = [[[] for i in range(x_n)]for j in range(y_n)]
        
        self.current = Pos(self.w//2,self.h//2)
        self.stack = []
        
    def get_available_neighbours(self, pos):
        n = []
        for p in ((-1,0),(1,0),(0,-1),(0,1)):
            pos_x = pos.x + p[0]
            pos_y = pos.y + p[1]
            if 0 <= pos_x < self.w and 0 <= pos_y < self.h and not self.flags[pos_y][pos_x]:
                n.append(Pos(pos_x,pos_y))
        return n
    
    def add_connection(self, pos_1, pos_2):
        self.nodes[pos_1.y][pos_1.x].append([pos_2.x, pos_2.y])
        self.nodes[pos_2.y][pos_2.x].append([pos_1.x, pos_1.y])
    
    def loop(self):
        if not self.flags[self.current.y][self.current.x]:
            self.flags[self.current.y][self.current.x] = True
        
        neighbours = self.get_available_neighbours(self.current)
        if len(neighbours) > 0:
            self.stack.append(self.current)
            rand_neighbour = random.choice(neighbours)
            temp = self.current
            self.current = rand_neighbour
            self.stack.append(self.current)
            self.add_connection(temp, self.current)
            self.draw_over_wall(temp, self.current)
            # self.draw_visit_line(temp, self.current)
        else:
            if len(self.stack) > 0:
                temp = self.current
                self.current = self.stack.pop()
                # self.draw_over_visit_line(temp, self.current)
            else:
                self.finished = True
                self.write_to_file()
                
                        
    def write_to_file(self):
        f = open("nodes.txt", "w")
        f.write('[\n')
        for y in range(self.h):
            for x in range(self.w):
                w_line = "["+str(x)+","+str(y)+"]"+str(self.nodes[y][x])
                f.write('{ x : '+str(x)+', y : '+str(y)+' , nodes : '+str(self.nodes[y][x])+' },\n')
                # print("[x: "+str(x)+"] [y: "+str(y)+"] "+str(self.nodes[y][x]))
                # print(w_line)
        f.write(']')
        f.close()
        print("File Written!!")
    
    def draw_over_visit_line(self, prev_pos, curr_pos):
        stroke(0)
        line(prev_pos.x*self.x_len+self.x_len/2,
             prev_pos.y*self.y_len+self.y_len/2, 
             curr_pos.x*self.x_len+self.x_len/2, 
             curr_pos.y*self.y_len+self.y_len/2)
        
    def draw_visit_line(self, prev_pos, curr_pos):
        # strokeWeight(7)
        stroke(0, 255, 255)
        # stroke(0)
        line(prev_pos.x*self.x_len+self.x_len/2,
             prev_pos.y*self.y_len+self.y_len/2, 
             curr_pos.x*self.x_len+self.x_len/2, 
             curr_pos.y*self.y_len+self.y_len/2)
    
    def draw_walls(self):
        walls = self.nodes
        stroke(255, 255, 255, 120)
        noFill()
        for x in range(self.w):
            for y in range(self.h):
                rect(x*self.x_len, y*self.y_len, self.x_len, self.y_len)
    
    def draw_over_wall(self, p_from, p_to):
        x = p_to.x - p_from.x
        y = p_to.y - p_from.y
        if x == 0 and y == 0:
            return
        pos_1 = None
        pos_2 = None
        if y < 0: #Top
            pos_1 = Pos(p_from.x * self.x_len + 1, p_from.y * self.y_len)
            pos_2 = Pos(p_from.x * self.x_len + self.x_len - 1, p_from.y * self.y_len)
        elif y > 0: #Bottom
            pos_1 = Pos(p_to.x * self.x_len + 1, p_to.y * self.y_len)
            pos_2 = Pos(p_to.x * self.x_len + self.x_len - 1, p_to.y * self.y_len)
        if x < 0: #Left
            pos_1 = Pos(p_from.x * self.x_len, p_from.y * self.y_len + 1)
            pos_2 = Pos(p_from.x * self.x_len, p_from.y * self.y_len + self.y_len - 1)
        elif x > 0: #Right
            pos_1 = Pos(p_to.x * self.x_len, p_to.y * self.y_len + 1)
            pos_2 = Pos(p_to.x * self.x_len, p_to.y * self.y_len + self.y_len - 1)
        # print(pos_1, pos_2)
        stroke(0)
        line(pos_1.x, pos_1.y, pos_2.x, pos_2.y)
        
        
        

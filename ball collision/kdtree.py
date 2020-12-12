import vector

max_balls = 10

def generate_kdtree(balls):
    return KDTree(0, balls)

def create_circle_query(pos, radius):
    return [pos[0], pos[1], radius]
    
class KDTree:
    def __init__(self, alignment, balls):
        self.balls = []
        self.alignment = alignment
        self.median_pos = None
        self.left = None
        self.right = None
        self.isDivided = False
        self.create(balls)
        
    def create(self, balls):
        if len(balls) < max_balls:
            self.balls = balls
        else:
            self.divide(balls)
            
    def divide(self, balls):
        self.isDivided = True
        balls.sort(key=lambda balls: balls.pos[self.alignment])
        mid = len(balls) // 2
        self.set_median_pos(balls, mid)
        self.left = KDTree((self.alignment + 1) % 2, balls[:mid])
        self.right = KDTree((self.alignment + 1) % 2, balls[mid:])

    def set_median_pos(self, balls, mid):
        median = balls[mid].pos[self.alignment]
        if len(balls) % 2 == 0:
            median_2 = balls[mid - 1].pos[self.alignment]
            median = (median + median_2) / 2
        self.median_pos = median
        
    def query(self, circle_query):
        query_res = []
        if not self.isDivided or self.intersect(circle_query):
            for ball in self.balls:
                if self.contains(circle_query, ball):
                    query_res.append(ball)
        if self.isDivided:
            if not self.is_target_left(circle_query):
                query_res += self.right.query(circle_query)
            if not self.is_target_right(circle_query):
                query_res += self.left.query(circle_query)
        # print("circle", circle_query, "res", query_res)
        # print("align", self.alignment, "pos", self.median_pos)
        return query_res
            
    def intersect(self, circle_query):
        return circle_query[self.alignment] - circle_query[2] < self.median_pos < circle_query[self.alignment] + circle_query[2]
        
    def contains(self, circle_query, ball):
        overlap = circle_query[2] + ball.radius - vector.distance_pos(circle_query, ball.pos)
        return overlap >= 0
        
    def is_target_left(self, circle_query):
        right_side = circle_query[self.alignment] + circle_query[2]
        return right_side < self.median_pos

    def is_target_right(self, circle_query):
        left_side = circle_query[self.alignment] - circle_query[2]
        return left_side >= self.median_pos

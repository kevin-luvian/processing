from ball import Ball
from random import randint, uniform
import kdtree

balls = []
target_point = [0,0]
circle_vision = 1
is_mouse_pressed = False

def setup():
    size(500, 500)
    
    for i in range(300):
        ball_size = uniform(4, 7)
        # ball_size = 4
        ball = Ball(randint(0,width), randint(0,height), ball_size)
        balls.append(ball)
    # big_ball = Ball(width/2, height/2, 30)
    # balls.append(big_ball)
        # print(ball_size)
        
    # balls.append(Ball(100, 100, 40))
    # balls.append(Ball(width/2, height/2, 40))
    # # balls.append(Ball(width/2 + 100, height/2 + 200, 7))
    # balls[0].set_heading([balls[1].pos[0], balls[1].pos[1] - 25], 1.3)
    # balls[1].set_heading([balls[0].pos[0], balls[0].pos[1]], 0)
    # balls[2].set_heading([balls[1].pos[0], balls[1].pos[1]], .6)
    
    textSize(32)
    background(0)

def draw():
    background(0)
    global is_mouse_pressed
    update_using_kdtree()
    # update_using_brute_force()
        
    for ball in balls:
        ball.update()
        ball.show()
        if is_mouse_pressed:
            ball.set_heading([mouseX, mouseY], 1)
            # ball.set_heading([width / 2, height / 2], 5)
    
    is_mouse_pressed = False
    fill(255, 255, 255, 190)
    text(str(ceil(frameRate)) + " fps", width - 130, height - 30)
    # if frameCount % 600 == 0:
    # background(0, 0, 0, .01)
    

def mouseClicked():
    global is_mouse_pressed
    is_mouse_pressed = True
    
        
def update_using_kdtree():
    # target_point = [width/2, height/2]
    kd_tree = kdtree.generate_kdtree(balls)
    for ball in balls:
        # ball.set_heading(target_point)
        vision = ball.radius * 2 * circle_vision
        if ball.radius > 20:
            vision = ball.radius * 2 * 1
        balls_near = kd_tree.query(kdtree.create_circle_query(ball.current_pos, vision))
        for other_ball in balls_near:
            if ball is not other_ball:
                ball.collide(other_ball)
                
def update_using_brute_force():
    for ball in balls:
        for other_ball in balls:
            if ball is not other_ball:
                ball.collide(other_ball)

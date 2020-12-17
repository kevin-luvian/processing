from maze_generator import Generator

g = None

def setup():
    size(1000, 500)
    background(0)
    global g
    x = 150
    y = 70
    g = Generator(width, height,x,y)
    g.draw_walls()
    # while(not g.finished):
    #     g.loop()
    # background(0)
    # print(g.flags)
    # print(g.walls)
    # print(g.walls[0][1])
    # g.draw_walls()
    frameRate(300)
    # noLoop()
    
def draw():
    # background(0)
    if not g.finished:
        g.loop()
    
    stroke(255)
    fill(0)
    rect(width - 140, height - 50, 70, 30)
    fill(0,255,255)
    text(str(ceil(frameRate)) + " fps", width - 130, height - 30)

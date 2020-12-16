import vector2d
from basic_shapes import SPoly

shapes = []

def setup():
    size(800, 500)
    shapes.append(SPoly(width/2 - 200,height/2,30,6))
    shapes[0].acc.add(vector2d.Vector(0, 1.5))
    shapes.append(SPoly(width/2,height/2,70,9))
    # shapes[0].vel.add(shapes[1].pos.copy().sub(shapes[0].pos).normalize().mult(10))
    
    # shapes.append(SPoly(width/2,height/2,100,5))
    # shapes.append(SPoly(170,100,40,11))
    # shapes.append(SPoly(70,400,50,5))
    frameRate(30)
    # noLoop()
    
def draw():
    background(0)
    # shapes[0].x = mouseX
    # shapes[0].y = mouseY
    # shapes[0].attract_to(mouseX, mouseY)
    
    shapes[0].attract_to(*(shapes[1].pos.get_val()))
    shapes[0].check_for_collisions(shapes)
    
    # for s in shapes:
        # s.attract_to(mouseX, mouseY)
        # s.check_for_collisions(shapes)
    
    for s in shapes:
        s.update()
        s.draw()
    

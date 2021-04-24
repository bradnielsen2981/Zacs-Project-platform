import random
import pygame
import pymunk
import pymunk.pygame_util
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
from pygame.locals import *
import math

collision_types = {
    "bin": 1,
    "ball": 2,
    "paddle": 3,
}

pygame.init()

#---------------------------------------------
#Ball object
class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y, radius = 25, mass = 10):
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.elasticity = 0.99
        self.shape.density = .0001
        self.shape.friction = 0.1 #add friction to shape 
        self.collision_type = collision_types["ball"]
        self.dead = False
        #checking to see if images work
        self.image = pygame.image.load("bball.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        return

    def add_to_space(self, space, table):
        space.add(self.body, self.shape)
        pivot = pymunk.PivotJoint(self.body, table, (0, 0), (0, 0))
        pivot.max_bias = 0  # disable joint correction
        pivot.max_force = 8  # emulate linear friction
        space.add(pivot)
        return

    def hit_ball(self, force, directionvector):
        forcevector = (force*directionvector[0],force*directionvector[1])
        self.body.apply_impulse_at_local_point(forcevector)
        print(forcevector)
        return

    def update(self, space): 
        self.rect.centery = self.body.position.y
        self.rect.centerx = self.body.position.x          
        if self.body.position.y > 700:
            space.remove(self.shape)
            space.remove(self.body)
            self.dead = True
        return

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return

#----------------------------------------------------------
#Bin Object
class Bin(object):

    def __init__(self, x, y, width, height):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 1.0
        self.shape.color = pygame.Color("blue")
        self.shape.group = 1
        self.shape.collision_type = collision_types["bin"]
        return

    def add_to_space(self, space):
        space.add(self.body, self.shape)
        #space.add(pivot)
        return

#sets up a new game
class Game(object):

    def __init__(self):
        self.space = pymunk.Space()

        self.table = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.position = 0, 0
        self.space.add(self.table) 
        #self.space.gravity = (0.0, 900.0)                             
        self.screen = pygame.display.set_mode((1024, 600))
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.add_static_scenery()
        self.ballsgroup = []
        self.selected_shapes = []
        self.running = True
        self.ticks_to_next_ball = 10
        self.active_shape = None
        self.dragging = False
        self.rotating = False
        self.platformRotations = []   
        return
    
    #game loop
    def run(self):

        #create bin
        bin = Bin(200, 500, 150, 300)
        bin.add_to_space(self.space)

        '''
        whiteball = Ball(20,200)
        whiteball.add_to_space(self.space)
        self.ballsgroup.append(whiteball)
        '''

        while self.running:
            self.process_events() #creates balls and updates paddles
            for ball in self.ballsgroup:
                ball.update(self.space)
                if ball.dead:
                    self.ballsgroup.remove(ball)

            self.clear_screen()
            self.draw_objects()
            
            self.space.step(1/60)
            self.clock.tick(60) #regulate speed
            pygame.display.flip() #flip the screen

    def add_static_scenery(self):
        self.linePoint1X = 50
        self.linePoint1Y = 100
        self.linePoint2X = 150
        self.linePoint2Y = 100
        return
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = event.pos
                shape = self.space.point_query_nearest(event.pos, float("inf"), pymunk.ShapeFilter()).shape
                if shape is not None and isinstance(shape, pymunk.Segment):
                    self.active_shape = shape
                    self.dragging = True
                    self.mouseMotion(event)
                    #print(self.active_shape)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.active_shape:
                        self.active_shape.rotation += 0.2
                        self.rotatePlatform()
                if event.key == pygame.K_RIGHT:
                    if self.active_shape:
                        self.active_shape.rotation -= 0.2
                        self.rotatePlatform()
                if event.key == pygame.K_n:
                    self.create_Platform() 
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:    
                    ball = Ball(50,200)
                    ball.add_to_space(self.space, self.table)
                    self.ballsgroup.append(ball)
                    directionvector = (random.randint(1,5),random.randint(-1,1))
                    ball.hit_ball(10,directionvector)
                if event.key == pygame.K_1:
                    pass
                    #self.ballsgroup[0].hit_ball(500,(5,0))
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging == True:
                    self.mouseMotion(event)    
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
        
        return
        
    def mouseMotion(self, event):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.space.remove(self.active_shape)
        self.active_shape.body.position = (self.mouse_x - self.linePoint1X,self.mouse_y + self.linePoint1Y)
        self.space.add(self.active_shape)
        return

    def create_Platform(self):
        static_body = self.space.static_body
        platformLine = pymunk.Segment(static_body, (self.linePoint1X, self.linePoint1Y), (self.linePoint2X, self.linePoint2Y), 7.0)
        platformLine.elasticity = .9
        platformLine.friction = 0.9
        platformLine.rotation = math.pi/2 
        self.space.add(platformLine)
        return

    def rotatePlatform(self):
        xc = (self.active_shape.a.x + self.active_shape.b.x) / 2
        yc = (self.active_shape.a.y + self.active_shape.b.y) / 2
        xa = xc - math.sin(self.active_shape.rotation)*50
        ya = yc - math.cos(self.active_shape.rotation)*50
        xb = xc + math.sin(self.active_shape.rotation)*50
        yb = yc + math.cos(self.active_shape.rotation)*50
        
        r = self.active_shape.rotation

        self.space.remove(self.active_shape)
        self.active_shape = pymunk.Segment(self.space.static_body, (xa, ya), (xb, yb), 7.0)
        self.active_shape.rotation = r
        self.space.add(self.active_shape)
        self.active_shape.elasticity = .9
        self.active_shape.friction = 0.9
        return

    def clear_screen(self):
        self.screen.fill(pygame.Color("white"))
        return

    def draw_objects(self):
        self.space.debug_draw(self.draw_options)
        for ball in self.ballsgroup:
            ball.draw(self.screen)
        return
        
if __name__ == "__main__":
    game = Game()
    game.run()
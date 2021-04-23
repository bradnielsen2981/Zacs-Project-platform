import pygame, sys, time, random
from pygame.locals import *




class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('platform.png').convert()
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

    def draw(self,surface):

            surface.blit(self.image,(self.x,self.y))


    def onKeyPress(self):

        key = pygame.key.get_pressed()
        distance = 5
        if key[ord('s')] or key[pygame.K_DOWN]: #down
            self.y += distance
        elif key[ord('w')] or key[pygame.K_UP]: #up
            self.y -= distance
        if key[ord('d')] or key[pygame.K_RIGHT]: #right
            self.x += distance
        elif key[ord('a')] or key[pygame.K_LEFT]: #left
            self.x -= distance

        rotate = pygame.transform.rotate
        if key[ord('e')]:
            self.image = rotate(self.image, 10)
        elif key[ord('q')]:
            self.image = rotate(self.image, -10)

class Event(object):

    def __init__(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


pygame.init()

fps = 30
fpsClock = pygame.time.Clock()

size = width,height = 800,600
screen = pygame.display.set_mode(size)
mySprite = MySprite()

while True:

    event = Event()
    screen.fill((0,255,0))

    mySprite.draw(screen)
    mySprite.onKeyPress()

    pygame.display.update()

    fpsClock.tick(fps)
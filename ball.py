import pygame
import math
import pymunk

class ball(pygame.sprite.Sprite):
    def __init__ (self, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ball2.png')
        self.surface = pygame.display.get_surface()
        self.vector = vector
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.dx = 0
        self.dy = 1
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.image.get_rect().height + self.rect.y > self.surface.get_height():
            self.dy *= -.8
            self.rect.y = self.surface.get_height() - self.image.get_rect().height
        self.dy += 1 

        self.rect.x += self.dx
        self.rect.y += self.dy        

    def calcnewpos(self,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))

    def move(self):
        self.update()
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        #pygame.draw.rect(self.surface,(0,0,255),self.rect)

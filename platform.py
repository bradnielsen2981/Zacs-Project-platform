import pygame
import math

class platform(pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.originalImage = pygame.image.load('platform.png')
        self.image = self.originalImage
        self.image.set_colorkey((0,0,20))
        self.rect_rotating = False
        self.rect_draging = False
        self.surface = pygame.display.get_surface()
        self.offset_x = 0
        self.offset_y = 0
        self.rect = self.image.get_rect()
        self.angle = 0
        self.x = 0
        self.y = 0
        self.mouse_x = 0
        self.mouse_y = 0

    

    def drag (self):

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    if self.rect.collidepoint(event.pos):
                        self.rect_draging = True
                        self.mouse_x, self.mouse_y = event.pos
                        self.offset_x = self.rect.x - self.mouse_x
                        self.offset_y = self.rect.y - self.mouse_y
                        
            
                elif event.button == 3:
                    if self.rect.collidepoint(event.pos):
                        self.rect_rotating = True
                        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:            
                    self.rect_draging = False

                elif event.button == 3:            
                    self.rect_rotating = False

            elif event.type == pygame.MOUSEMOTION:
                if self.rect_draging:
                    self.mouse_x, self.mouse_y = event.pos
                    self.rect.x = self.mouse_x + self.offset_x
                    self.rect.y = self.mouse_y + self.offset_y

                elif self.rect_rotating:
                    tempx, tempy = event.pos
                    distance = ((tempx - self.mouse_x)**2 + (tempy - self.mouse_y)**2)**0.5
                    self.angle = distance

            elif event.type == pygame.QUIT:
                return False
        return True            

    def move (self):
        self.drawrect()


    
    def drawrect (self):

        self.image = pygame.transform.rotate(self.originalImage, int(self.angle))
        halfwidth = int(self.image.get_width()/2)
        halfheight = int(self.image.get_height()/2)
        self.rect.height = self.image.get_height()
        self.rect.width = self.image.get_width()
        pygame.draw.rect(self.surface,(0,0,255),self.rect)
        self.surface.blit(self.image,(self.rect.x, self.rect.y))

        
        
        

 
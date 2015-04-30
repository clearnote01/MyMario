import pygame
import sys
import pygame
import time
from pygame.locals import *


pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
RED_LIGHT = (255,128,125)
BLUE = (180, 200, 255)
GREY = (121, 121, 121)
BROWN = (108, 88, 90, 255)
DARKGREY = (60, 60, 60)
LIGHT_BROWN = (255, 176, 75)
SKY_BLUE = (155, 255, 255)
width, height = 32*42, 32*22
FPS = 100



soundObj = pygame.mixer.Sound('coin.ogg')
pygame.display.set_caption("Real_B")
#pygame.mixer.music.load('chandelier.mp3')
fpsClock = pygame.time.Clock()
#pygame.mixer.music.play(1, 0.-1)



def safelyexit():
    pygame.quit()
    sys.exit()

class Map(pygame.sprite.Sprite):

    def __init__(self):

        #self.sky = pygame.Surface((32, 32))
        #self.sky.fill(BLUE)
        self.surfbase = pygame.Surface((32, 32))
        self.platf = pygame.Surface((32, 32))
        self.surfbase.fill(LIGHT_BROWN)
        self.platf.convert_alpha()
        self.platf.fill(LIGHT_BROWN)
        self.platform = []
        self.rec = []
        self.l = []
        self.platfrm = []


    def initplatform(self):
        self.platform.append(self.rec[20][0])
        self.platform.append(self.rec[0][0])
        self.platform.append(self.rec[1][0])
        self.platform.append(self.rec[1][41])
        for i in range(len(self.platfrm)):
            self.platform.append(self.platfrm[i][0])
        print self.platform[3]
        print self.platform[0]


#there is some bug here, platform[2] is not correct hence i have given it a dummy value

    def makeplatform(self):
        self.platform[0].unionall_ip(self.rec[20])    #base line
        self.platform[1].unionall_ip(self.rec[0])     #top most line
        for i in range(19):
            self.platform[2].union_ip(self.rec[i+1][0])
            self.platform[3].union_ip(self.rec[i+1][41])
        print self.platform[3]
        print self.platform[2]
        print 'kj'
        for i in range(len(self.platfrm)):
            self.platform[i+4].unionall_ip(self.platfrm[i])




class Ball(pygame.sprite.Sprite):

    def __init__(self, SCREEN, inip):

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.falling = False
        self.jumping = False
        self.rekt = pygame.Rect(inip[0],inip[1],32, 32)
        self.olrekt = pygame.Rect(inip[0],inip[1],32,32)
        self.imgl = pygame.Surface((32, 32))
        self.imgrr = pygame.Surface((32, 32))
        self.surf = pygame.Surface((32, 32))
        self.jump = 0
        self.v_y = 300
        self.v_x = 3
        self.grounded = True
        self.gravity = 500
        self.timery = pygame.time.get_ticks()/1000.0
        self.timerz = pygame.time.get_ticks()/1000.0
        self.posy = 0
        self.posx = 0
        self.i = 0

    def timers(self, dirac):
        if dirac == 2:  #up
            self.timery = pygame.time.get_ticks()/1000.0
        if dirac == 1:  #left
            self.timerx = pygame.time.get_ticks()/1000.0
        if dirac == -1: #right
            self.timerl = pygame.time.get_ticks()/1000.0
        if dirac == 0:  #falling
            self.timerz = pygame.time.get_ticks()/1000.0

    def move(self):
        if self.up == True:
            t = pygame.time.get_ticks()/1000.0 - self.timery
            self.rekt.bottom = self.posy - float(self.v_y*t) + (1.0/2)*float(self.gravity*t*t)


        """if dirac == 0:
            t = pygame.time.get_ticks()/1000.0 - self.timerz
            self.posy = self.newpos - (1.0/2)*float(self.gravity*t*t)
"""
        if self.right == True:

            self.rekt.right +=  self.v_x

        if self.left == True:
            self.rekt.left -=  self.v_x

        if self.down == True:
            t = pygame.time.get_ticks()/1000.0 - self.timerz
            self.rekt.bottom = self.posx + (1.0/2)*float(self.gravity*t*t)

    def update(self, SCREEN):
        if self.right== True:
            self.surf = self.imgrr
        if self.left== True:
            self.surf = self.imgl
        SCREEN.blit(self.surf, (self.rekt.topleft))

    def hitground(self, platform):
        for i in range(len(platform)):
            if self.rekt.colliderect(platform[i]):
                if self.rekt.bottom >= platform[i].top and self.rekt.top <= platform[i].top:
                    self.up = False
                    self.down = False
                    self.rekt.bottom = platform[i].top
                    self.jump = 0
                    self.i = i

                if self.rekt.top <= platform[i].bottom and self.rekt.bottom >= platform[i].bottom and self.down ==False:
                    self.down = True
                    self.timers(0)
                    self.rekt.top = platform[i].bottom
                    self.posx = self.rekt.bottom

                """if self.rekt.right >= platform[i].left and self.rekt.left <= platform[i].left:
                    self.down = True
                    self.timers(0)
                    self.rekt.right = platform[i].left
                    self.posx = self.rekt.bottom

                if self.rekt.left <= platform[i].right and self.rekt.right >= platform[i].left:
                    self.down = True
                    self.timers(0)
                    self.rekt.right = platform[i].left
                    self.posx = self.rekt.bottom
"""

def main():
    surfaru = pygame.display.set_mode((width, height))
    surface = pygame.Surface((width, height))
    surface.fill(BLUE)

    maplvl = Map()
    ball= Ball(surface, (2*32, 19*32))

    try:
        #ball.imgl = pygame.image.load('priyamt50.png')
        #ball.imgrr = pygame.image.load('priyamt50l.png')
        pygame.draw.rect(ball.imgl, BLACK, (0,0, 32, 32))
        pygame.draw.rect(ball.imgrr, BLACK, (0,0, 32, 32))

    except:
        print 'Image not loading'
        safelyexit()
    ball.surf = ball.imgrr
    l = [(2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2),#0
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),#4
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,2),#9
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),#14
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,2),#15
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),
         (2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2),#19
         (2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2),
         (2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2),
                                     #15

         ]
    maplvl.platfrm = []

    for y in range(len(l)):
        reclist = []
        platrr = []

        for x in range(len(l[y])):
            rec = pygame.Rect((x*32, y*32, 32, 32))
            reclist.append(rec)
            if l[y][x]==0:
                surface.blit(maplvl.surfbase, (x*32, y*32))
                platrr.append(rec)
            if l[y][x]==2:
                surface.blit(maplvl.platf, (x*32, y*32))
                pygame.draw.rect(surface, BLACK, rec, 2)
            if l[y][x]!=0 and l[y][x-1]==0:
                maplvl.platfrm.append(platrr)
                platrr = []
        maplvl.rec.append(reclist)
    maplvl.initplatform()
    maplvl.makeplatform()

       #ground

    print maplvl.platform[4]
    print ball.rekt.bottom
    i = 0
    #for
    while True:
        surfaru.fill(WHITE)
        surfaru.blit(surface, (0,0))
        ball.update(surfaru)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                safelyexit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    safelyexit()
                if event.key == K_UP and (ball.jump == 1 or ball.up==False):
                    ball.timers(2)
                    ball.up = True
                    ball.posy = ball.rekt.bottom
                    ball.i = -1
                    ball.down = False
                if event.key == K_RIGHT and ball.right == False:
                    ball.right = True
                if event.key == K_LEFT and ball.left==False:
                    ball.left = True
                """if event.key == K_w and ((ball2.grounded == True or ball2.jump == 1) or ball2.falling==True):
                    ball2.goup()
                if event.key == K_d and ball2.right==False:
                    ball2.goright()
                if event.key == K_a and ball.left==False:
                    ball2.goleft()"""
            if event.type == KEYUP:
                if event.key == K_UP:
                    ball.jump += 1
                if event.key == K_LEFT:
                    ball.left = False
                if event.key == K_RIGHT:
                    ball.right = False

        if ball.up == True or ball.down == True:
            ball.hitground(maplvl.platform)

        if ball.i in range(len(maplvl.platform)) and ball.down == False:
            if ball.rekt.left >= maplvl.platform[ball.i].right or ball.rekt.right <= maplvl.platform[ball.i].left:
                ball.down = True
                ball.timers(0)
                ball.posx = ball.rekt.bottom
                print ball.i


                ball.i = -1
                ball.jump -= 1
                print ball.i
        ball.move()
        pygame.display.update()
        fpsClock.tick(FPS)
main()

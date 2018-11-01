# -*- coding: UTF-8 -*-
#------------------- Bool Robot -------------------#
# Author: Alex, Li Chao
# Date:   Jun 26,2018
#
# CHANGE:
# 1.Add key press detection
### ======================================================================
import random,sys,time,pygame
from pygame.locals import *
import numpy as np
import math
### ======================================================================
CELLSIZE = 20
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
DIAMOND_SIZE = 8

assert WINDOWWIDTH % CELLSIZE  == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window hight must be a multiple of cell size."

CELLWIDTH = int(WINDOWWIDTH /CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

BLACK        = (0,0,0)
RED          = (255,0,0)
GREEN        = (0,255,0)
BLUE         = (0,0,255)
DARKGREEN    = (0,155,0)
DARKGRAY     = (40,40,40)
WHITE        = (255,255,255)
BGCOLOR      = BLACK

BLOCK_BLACK     = 0
BLOCK_RED       = 1
BLOCK_GREEN     = 2
BLOCK_BLUE      = 3
BLOCK_DARKGREEN = 4
BLOCK_DARKGRAY  = 5
BLOCK_WHITE     = 6
# BLOCK_COLOR_S = {'WHITE':WHITE,'BLACK':BLACK,'RED':RED,'GREEN':GREEN,'BLUE':BLUE,
                # 'DARKGREEN':DARKGREEN,'DARKGRAY':DARKGRAY}
BLOCK_COLOR_STR = {'BLACK':0,'RED':1,'GREEN':2,'BLUE':3,'DARKGREEN':4,'DARKGRAY':5,'WHITE':6}
BLOCK_COLOR_N   = {0:'BLACK',1:'RED',2:'GREEN',3:'BLUE',4:'DARKGREEN',5:'DARKGRAY',6:'WHITE'}
BLOCK_COLOR_NUM = {0:BLACK, 1:RED, 2:GREEN, 3:BLUE, 4:DARKGREEN, 5:DARKGRAY, 6:WHITE}

FRONT  = 'front'
BACK   = 'back'
LEFT   = 'left'
RIGHT  = 'right'

ORI_NORTH = 0
HEAD = "north"

### ======================================================================
# Test:create a map
map_2 = np.zeros([CELLSIZE,CELLSIZE],int)
map_2[10,10] = 1
map_2[2,2] = 2
map_2[9,9] = 1


### ======================================================================
class boolgamecar:
    ''' You can manipulate the car to do a lot amazing things! '''
    def __init__(self):
        global FPSCLOCK,DISPLAYSURF,BASICFONT
        self.FPS = 1
        ### The Car position is defined by (position_x,position_y), while belong to (1,1) to (CELLWIDTH,CELLHEIGHT)
        self.position_x = 0
        self.position_y = 0
        self.flag_x =0
        self.flag_y=0
        self.map_zero = np.zeros([CELLWIDTH,CELLHEIGHT],int)
        self.map = self.map_zero
        self.car_picname = "car_red"
        #self.car_pic = pygame.image.load("BoolCar game/resources/car_red.png")
        self.car_pic = pygame.image.load("resources/car_red.png")
        ### ////////////////////////////////////
        #             0 north
        #                ^
        #   3 west <- carhead -> 1 east
        #                ^
        #             2 south
        self.car_heading = 0
        self.car_heading_to = ["NORTH","EAST","SOUTH","WEST"]
        self.mat_move_front = [[0,-1],[1,0],[0,1],[-1,0]]
        self.mat_move_back  = [[0,1],[-1,0],[0,-1],[1,0]]
        self.mat_move_right = [[1,0],[0,1],[-1,0],[0,-1]]
        self.mat_move_left  = [[-1,0],[0,-1],[1,0],[0,1]]
        ### ////////////////////////////////////
        pygame.init()
        FPSCLOCK= pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
        #BASICFONT = pygame.font.Font('BoolCar game/resources/ARBERKLEY.ttf',18)
        BASICFONT = pygame.font.Font('resources/ARBERKLEY.ttf',18)
        pygame.display.set_caption('BoolCar Game')
        
        DISPLAYSURF.fill(BGCOLOR)
        self.__drawGrid()

    def update_state(self):
        ### ////////////////////////////////////
        ### Adding event is necessary to keep game running
        for event in pygame.event.get():
            self.getkeypress(event)
            #print(self.__checkForKeyPress())
            pass
        DISPLAYSURF.fill(BGCOLOR)
        self.__drawMap(self.map)
        self.__drawCar()

        self.__drawGrid()
        pygame.display.update()
        FPSCLOCK.tick(self.FPS)

    ### -----------------------------------------------------------------
    ### private function
    def __drawMap(self,map):
        for x in range(0,CELLWIDTH):
            for y in range(0,CELLHEIGHT):
                shape = BLOCK_COLOR_NUM[map[y][x]]
                if shape == RED or shape == BLACK:
                    self.__drawBlock(x,y,shape)
                else:
                    self.__drawDiamond(x,y,BLOCK_COLOR_NUM[map[y][x]])

    def __drawGrid(self):
        for x in range(0,WINDOWWIDTH,CELLSIZE):
            pygame.draw.line(DISPLAYSURF,DARKGRAY,(x,0),(x,WINDOWHEIGHT))
        for y in range(0,WINDOWHEIGHT,CELLSIZE):
            pygame.draw.line(DISPLAYSURF,DARKGRAY,(0,y),(WINDOWWIDTH,y))

    def __drawBlock(self,x,y,color):
        # (x,y) is left-up corner's position
        x = x*CELLSIZE
        y = y*CELLSIZE
        blockRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
        pygame.draw.rect(DISPLAYSURF,color,blockRect)
    def __drawDiamond(self,x,y,color):
        x_center = x*CELLSIZE + CELLSIZE//2
        y_center = y*CELLSIZE + CELLSIZE//2
        pygame.draw.polygon(DISPLAYSURF,color,
                            [[x_center,y_center-DIAMOND_SIZE],[x_center+DIAMOND_SIZE,y_center],\
                            [x_center,y_center+DIAMOND_SIZE],[x_center-DIAMOND_SIZE,y_center]])

    def __drawCar(self):
        #self.__drawBlock(x,y,GREEN)
        x = self.position_x*CELLSIZE
        y = self.position_y*CELLSIZE
        if self.car_picname == "":
            carRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
            pygame.draw.rect(DISPLAYSURF,WHITE,carRect)
        else:
            DISPLAYSURF.blit(self.car_pic,[x,y])

    def __checkForKeyPress(self):
        if len(pygame.event.get(QUIT)) > 0:
            self.__terminate()
        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            self.__terminate()
        return keyUpEvents[0].key

    def __terminate(self):
        pygame.quit()
        sys.exit()
    
    def __validate_range(self,range_low,range_high,value):
        if value in range(range_low,range_high):
            return True
        else:
            return False
    def __validate_position(self,x,y):
        if x not in range(0,CELLWIDTH) or y not in range(0,CELLHEIGHT):
            return False
        else:
            return True
        
    ### -----------------------------------------------------------------
    ### public function
    def getkeypress(self,event):
        if event.type==QUIT:
            self.__terminate()
        self.key=pygame.key.get_pressed()
        if self.key[K_ESCAPE]:
            self.__terminate()
    ### ////////////////////////////////////
    def set_car_speed(self,speed=1):
        self.FPS = speed
    def set_car_position(self,pos=[0,0]):
        self.position_x = pos[0]
        self.position_y = pos[1]
    def load_map(self,map):
        self.map = map
    def delete_map(self):
        self.map = self.choose_map

    ### ////////////////////////////////////
    ### move BoolCar
    def front_blocked(self):
        x = self.position_x + self.mat_move_front[self.car_heading][0]
        y = self.position_y + self.mat_move_front[self.car_heading][1]
        if self.map[y][x] == BLOCK_COLOR_STR["RED"]:
            return True
        if x not in range(0,CELLWIDTH) or y not in range(0,CELLHEIGHT):
            return True
        else:
            return False
    def back_blocked(self):
        x = self.position_x + self.mat_move_back[self.car_heading][0]
        y = self.position_y + self.mat_move_back[self.car_heading][1]
        if self.map[y][x] == BLOCK_COLOR_STR["RED"]:
            return True
        if x not in range(0,CELLWIDTH) or y not in range(0,CELLHEIGHT):
            return True
        else:
            return False
    def right_blocked(self):
        x = self.position_x + self.mat_move_right[self.car_heading][0]
        y = self.position_y + self.mat_move_right[self.car_heading][1]
        if self.map[y][x] == BLOCK_COLOR_STR["RED"]:
            return True
        if x not in range(0,CELLWIDTH) or y not in range(0,CELLHEIGHT):
            return True
        else:
            return False
    def left_blocked(self):
        x = self.position_x + self.mat_move_left[self.car_heading][0]
        y = self.position_y + self.mat_move_left[self.car_heading][1]
        if self.map[y][x] == BLOCK_COLOR_STR["RED"]:
            return True
        if x not in range(0,CELLWIDTH) or y not in range(0,CELLHEIGHT):
            return True
        else:
            return False
    def move_front(self):
        if not self.front_blocked():
            self.position_x += self.mat_move_front[self.car_heading][0]
            self.position_y += self.mat_move_front[self.car_heading][1]
        else:
            print("Car has block in front!")
        self.update_state()
    def move_back(self):
        if not self.back_blocked():
            self.position_x += self.mat_move_back[self.car_heading][0]
            self.position_y += self.mat_move_back[self.car_heading][1]
        else:
            print("Car has block in back!")
        self.update_state()
    def turn_left(self):
        self.car_heading -= 1
        if self.car_heading < 0:
            self.car_heading = 3
        self.car_pic = pygame.transform.rotate(self.car_pic,90)
        self.update_state()
    def turn_right(self):
        self.car_heading += 1
        if self.car_heading > 3:
            self.car_heading = 0
        self.car_pic = pygame.transform.rotate(self.car_pic,-90)
        self.update_state()
    def turn_around(self):
        self.turn_right()
        self.turn_right()

    def heading_to(self):
        return self.car_heading_to[self.car_heading]
    ### ////////////////////////////////////
    ### manipulate diamonds
    def diamond_present(self):
        if self.map[self.position_y][self.position_x] > 1:
            return True
        else:
            return False
    def delete_diamond(self):
        if self.diamond_present():
            x = self.position_x
            y = self.position_y
            self.map[y][x] = 0
        else:
            print("No diamond here to delete!")
    def put_diamond(self,color):
        if not self.diamond_present():
            diamond_color = BLOCK_COLOR_STR[color]
            self.map[self.position_y][self.position_x] = diamond_color
        else:
            print("A diamond alread here, can't put more!")
    def get_diamond_color(self):
        color = BLOCK_COLOR_N[self.map[self.position_y][self.position_x]]
        if color != "BLACK":
            return color
        else:
            return "None"
    def change_diamond_color(self,color):
        if self.diamond_present():
            diamond_color = BLOCK_COLOR_STR[color]
            self.map[self.position_y][self.position_x] = diamond_color
        else:
            print("No diamond here to change color!")

    ### ////////////////////////////////////
    ### manipulate blocks
    def detect_block(self):
        return BLOCK_COLOR_N[self.map[self.position_y][self.position_x]]
    
    def change_block(self,color='BLACK'):
        self.map[self.position_y][self.position_x] = BLOCK_COLOR_STR[color]

from boolgame import *
import numpy as np
from maps import map_putDiamonds,map_changeColor,map_maze

### ======================================================================
##  1:'RED',2:'GREEN',3:'BLUE',4:'DARKGREEN',5:'DARKGRAY',6:'WHITE'
car = boolgamecar()

def myFunction():
    car.set_car_speed(1)
    car.load_map(map_changeColor)
    finished = False
    while True: 
        if not finished:       
            car.turn_right()
            for i in range(0,7):
                car.move_front()
            car.turn_right()
            for i in range(0,6):
                car.move_front()
            finished = True 
        else:
            car.update_state()
def putDiamonds():
    car.set_car_speed(1)
    car.load_map(map_putDiamonds)
    car.set_car_position([5,5])
    finished = False
    while True:
        if not finished:
        ###======================================###
        ### type in our code here                ###
            car.turn_right()
            for i in range(0,12):
                if i%2 == 0:
                    car.put_diamond("BLUE")
                car.move_front()

            car.turn_left()
            car.move_front()
            finished = True
        ###======================================###
        else:
            car.update_state()

def getout_maze():
    car.set_car_speed(1)
    car.set_car_position([4,3])
    car.load_map(map_maze)
    finished = False
    car.turn_right()
    car.turn_right()
    while True:
        if not finished:
            car.delete_diamond()
            ###======================================###
            ### type in our code here                ###
            while "BLUE" != car.get_diamond_color():
                if not car.left_blocked():
                    car.turn_left()
                if car.front_blocked():
                    car.turn_right()
                car.move_front()
                finished = True
            ###======================================###
        else:
            car.update_state()
def key_press():
    car.set_car_speed(10)
    car.load_map(map_maze)
    while True:
        car.update_state()
        if car.key[K_w]:
            car.move_front()
        elif car.key[K_a]:
            car.turn_left()
        elif car.key[K_s]:
            car.move_back()
        elif car.key[K_d]:
            car.turn_right()
if __name__ == '__main__':
    #putDiamonds()
    key_press()


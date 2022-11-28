import math
from canvas_properties import *
from assets import *
from random import choice, randint, random


belts = {1: {'y': 185, 'speed': 300, 'miss_probability':0.04},
         2: {'y': 385, 'speed': 200, 'miss_probability':0.08},
         3: {'y': 585, 'speed': 400, 'miss_probability':0.04}}

class Simulator_Object:

    def __init__(self, obj_name, x, y, speedx=0, speedy=0, rot=0, width=100, height=100):
        self.obj_class = obj_name.split('/')[0]
        self.object = obj_name
        self.rot = (rot * math.pi) / 180
        self.height = height
        self.width = width
        self.speedx = speedx
        self.speedy = speedy
        self.x = x
        self.y = int(y)
        self.hitbox = {"x": int(x + width / 2), "y": int(y + height / 2), "radius": 50}

    def get_state(self):
        return [self.x, self.y, self.speedx, self.speedy]

    def __contains__(self, item):
        if type(item) is Simulator_Object or type(item) is Trash_Object:
            return bool(
                self.x + self.width > item.hitbox["x"] > self.x and self.y + self.height > item.hitbox["y"] > self.y)

    def checkCoordinateIntersection(self, x, y):
        dist = math.sqrt(math.pow(abs(self.hitbox["x"] - x), 2) + math.pow(abs(self.hitbox["y"] - y), 2))
        return dist < self.hitbox["radius"]

    def setSpeed(self, speed_X, speed_y=0):
        self.speedx = speed_X
        self.speedy = speed_y


class Belt(Simulator_Object):
    def __init__(self, belt_number, timestep_size, x=-50, speedx=0, speedy=0, rot=0, width=CANVAS_WIDTH + 150,
                 height=160):

        self.obj_name = 'ConvBeltNew'
        self.y = belts[belt_number]['y']
        self.belt_speed = belts[belt_number]['speed'] * timestep_size
        self.miss_probability = belts[belt_number]['probability']

        super().__init__(self.obj_name, x, self.y, speedx, speedy, rot, width, height)


def initialize_belts(timestep_size):
    belts = []
    for belt in range(1, 4):
        belts.append(Belt(belt, timestep_size))
    return belts


class Trash_Object(Simulator_Object):
    def __init__(self, obj_name, env, belt, speedy=0, width=100, height=100):
        env.n_trash_objects += 1
        self.x = -100 - randint(0, 150)
        self.y = belt.y + 25
        self.speedx = belt.belt_speed
        self.rot = randint(-90, 90)
        super().__init__(obj_name, self.x, self.y, self.speedx, speedy, self.rot, width, height)
        self.deleted = False
        self.miss_probability = belt.miss_probability * trash_visibility[obj_name]

        self.row = -999
        self.column = -999
        if self.obj_class == 'reject':
            env.n_unrecyclable_objects += 1

    def getCell(self):
        y_cells = {250: 0, 450: 1, 650: 2}
        return y_cells[self.hitbox['y']], math.floor((self.hitbox['x'] + 250) / 100)  # row, col

    def update_position(self, env):
        self.x = self.x + self.speedx
        self.y = self.y + self.speedy
        self.hitbox["x"] += self.speedx
        self.hitbox["y"] += self.speedy
        self.row, self.column = self.getCell()
        if self.column > 32:
            self.column = 32
            env.off_screen['recyclable' if self.obj_class != 'reject' else 'reject'].append(self)
        env.full_grid_state[self.row][self.column][int(self.obj_class != 'reject')] += 1
        env.full_element_state[self.row][self.column].append(self)

    def set_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.hitbox = {"x": int(new_x + self.width / 2), "y": int(new_y + self.height / 2), "radius": 50}

    def dragToTrash(self):
        self.x = 1512
        self.y = 90
        self.hitbox = {"x": int(self.x + self.width / 2), "y": int(self.y + self.height / 2), "radius": 50}
        self.speedx = 0
        self.speedy = 0

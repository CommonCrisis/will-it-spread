import numpy as np
import pyglet
from pyglet.window import key
from pathlib import Path

from utils.globals import GLOBAL_X, GLOBAL_Y, TILE_SIZE, TIME_RANGE
from classes.simulation import Simulation

data_folder = Path('img/tiles/')

red_tile = data_folder / 'red_tile.png'
blue_tile = data_folder / 'blue_tile.png'

window = pyglet.window.Window(GLOBAL_X * TILE_SIZE, GLOBAL_Y * TILE_SIZE)
red = pyglet.image.load(red_tile)
blue = pyglet.image.load(blue_tile)



def tile_mapping(color, x, y):
    if color == 'red':
        return red.blit(x, y)
    elif color == 'blue':
        return blue.blit(x, y)

    return


num_mapping = {0: 'blue', 1: 'red', 2: 'black'}

### init simulation ###

simulation = Simulation()


@window.event
def on_draw():
    window.clear()
    simulation.update()
    for (x, y), value in np.ndenumerate(simulation.world.translate_world()):
        tile_mapping(num_mapping[value], x * TILE_SIZE, y * TILE_SIZE)


while True:
    if simulation.check_all_alive() or simulation.check_all_dead():
        break
    
    if simulation.day_counter == TIME_RANGE:
        print('Time over')

    pyglet.clock.tick()

    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()
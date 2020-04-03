import numpy as np
from classes.human import Human
from classes.world import World
from utils.randomizer import create_chance
from typing import List
from utils.globals import (
    HUMAN_MOVEMENT,
    GLOBAL_X,
    GLOBAL_Y,
    TIME_UNTIL_CURED,
    CHANCE_CURE,
    TIME_UNTIL_DEATH,
    CHANCE_DEATH,
    HUMANS,
    TIME_RANGE,
)
import random as rnd 

class Simulation:
    def __init__(self):
        self.world = World(GLOBAL_X, GLOBAL_Y)
        self.init_population()
        self.start_population = sum(list(self.count_humans().values()))
        self.humans_on_grid_vec = np.vectorize(self._update_humans_on_grid)
        self.update_human_vec = np.vectorize(self._update_human)
        self.day_counter = 0

    def init_population(self):

        current_grid = self.world.world_grid

        for _ in range(0, HUMANS):
            x = rnd.randint(0, GLOBAL_X - 1)
            y = rnd.randint(0, GLOBAL_Y - 1)
            is_sick = create_chance(0.01)
            if not current_grid[x, y]:
                current_grid[x, y] = Human(x, y, is_sick)

    def _update_human(self, val):
        if val:
            if val.is_sick:
                if val.sick_days >= TIME_UNTIL_CURED:
                    if create_chance(CHANCE_CURE):
                        val.cure()
                val.sick_days += 1
                if val.sick_days >= TIME_UNTIL_DEATH and val.is_sick:
                    if create_chance(CHANCE_DEATH):
                        val.die()

    def update_humans_vec(self):
        return self.update_human_vec(self.world.world_grid)

    def _get_random_humans(self, human_positions: List[List[str]]):
        positions = np.transpose((human_positions).nonzero()).tolist()
        random_humans = [rnd.choice(positions) for p in range(HUMAN_MOVEMENT)]

        return random_humans

    def _update_humans_on_grid(self, val):
        if val:
            if val.is_dead:
                self.world.world_grid[val.pos_x, val.pos_y] = None

    def update_humans_on_grid_vec(self):
        return self.humans_on_grid_vec(self.world.world_grid)

    def update(self):
        for human in self._get_random_humans(self.world.world_grid):
            x, y = human
            m_x = rnd.randint(-1, 1)
            m_y = rnd.randint(-1, 1)
            if self.world.world_grid[x, y]:
                self.world.world_grid[x, y].move(m_x, m_y, self.world.world_grid)
        self.update_humans_vec()
        self.update_humans_on_grid_vec()
        self.day_counter += 1

    def count_humans(self, ignore_empty: int = 2):
        unique, counts = np.unique(self.world.translate_world(), return_counts=True)
        data = dict(zip(unique, counts))
        del data[ignore_empty]
        return data

    def check_all_alive(self):
        if not self.count_humans().get(1):
            print('All people are healthy')
            print(f'{(1-(self.count_humans().get(0)/self.start_population))*100} % died')

            return True
        return False

    def check_all_dead(self):
        if not self.count_humans().get(0):
            print('All people are dead')

            return True
        
        return False

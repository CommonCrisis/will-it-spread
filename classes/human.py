from utils.globals import GLOBAL_X, GLOBAL_Y, CHANCE_CURE
import numpy as np


class Human:
    def __init__(self, pos_x: int, pos_y: int, is_sick: bool):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_sick = is_sick
        self.is_dead = False
        self.sick_days = 0
        self.in_hospital = False
        self.chance_to_cure = CHANCE_CURE

    def __str__(self):
        if self.is_sick:
             return f'Human on postition {self.pos_x, self.pos_y} is sick for {self.sick_days} days'
        else:
             return f'Human on postition {self.pos_x, self.pos_y} is not sick'

    def get_sick(self):
        self.is_sick = True

    def cure(self):
        self.is_sick = False

    def die(self):
        self.is_dead = True

    def _check_new_pos(self, new_pos: int, global_limit: int) -> int:
        if new_pos >= global_limit - 1:
            return global_limit - 1
        elif new_pos <= 0:
            return 0
        else:
            return new_pos

    def _infect(self, pos_x: int, pos_y: int, grid: np.array):
        grid[pos_x, pos_y].is_sick = True

        return grid

    def move(self, x: int, y: int, grid: np.array):
        if self.in_hospital:
            return grid

        new_x = self._check_new_pos(self.pos_x + x, GLOBAL_X)
        new_y = self._check_new_pos(self.pos_y + y, GLOBAL_Y)
        if type(grid[new_x, new_y]) == Human:
            if not self.is_sick:
                return grid
            grid = self._infect(new_x, new_y, grid)
            return grid

        grid[self.pos_x, self.pos_y] = None
        self.pos_x = new_x
        self.pos_y = new_y
        grid[self.pos_x, self.pos_y] = self

        return grid


class Doctor(Human):
    def __init__(self, pos_x: int, pos_y: int, is_sick: bool, skill: int):
        Human.__init__(self, pos_x, pos_y, is_sick)
        self.in_hospital = True
        self.skill = skill
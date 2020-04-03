import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import pandas as pd
from typing import List

from utils.globals import *
from utils.randomizer import create_chance
from classes.human import Human
from classes.world import World


world = World(GLOBAL_X, GLOBAL_Y)
grid = world.world_grid


def _get_random_humans(human_positions: List[List[str]]):
    positions = np.transpose((human_positions).nonzero()).tolist()
    random_humans = [rnd.choice(positions) for p in range(HUMAN_MOVEMENT)]

    return random_humans


def update_human(val, TIME_RANGE: int):
    if val:
        if val.is_sick:
            if val.sick_days >= TIME_UNTIL_CURED:
                if create_chance(CHANCE_CURE):
                    val.cure()
            val.sick_days += 1
            if val.sick_days >= TIME_UNTIL_DEATH and val.is_sick:
                if create_chance(CHANCE_DEATH):
                    val.die()


def grid_to_array_sick(val):
    if val:
        if val.is_sick:
            return 1
        else:
            return -1
    return 0


def count_humans(grid: np.array):
    unique, counts = np.unique(grid, return_counts=True)
    data = dict(zip(unique, counts))
    del data[0]
    return data


def time_sick_correlation(time_line: dict):
    df = pd.DataFrame.from_dict(time_line, orient='index', columns=['all_humans', 'sick_humans'])
    df['time_step'] = df.index

    return df


map_humans = np.vectorize(grid_to_array_sick)
update_humans = np.vectorize(update_human)
update_grid = np.vectorize(world.update)


sickness = {
    True: 2,
    False: 1,
}

for p in range(0, HUMANS):
    x = rnd.randint(0, GLOBAL_X - 1)
    y = rnd.randint(0, GLOBAL_Y - 1)
    is_sick = create_chance(0.1)
    if not grid[x, y]:
        grid[x, y] = Human(x, y, is_sick, sickness[is_sick])


fig, axs = plt.subplots(ncols=2)
fig = plt.gcf()
fig.show()
fig.canvas.draw()
colors = ['#FFFFFF', '#3EB24E', '#7FFF00', '#B3B3B3', '#CC0000']

time_line = {}

collected_humans = map_humans(grid)
start_pop = sum(list(count_humans(collected_humans).values()))
for idx in range(TIME_RANGE):
    collected_humans = map_humans(grid)
    if not count_humans(collected_humans).get(1):
        print('All people are healthy')
        print(f'{(1-(count_humans(collected_humans).get(-1)/start_pop))*100} % died')
        break
    if not count_humans(collected_humans).get(-1):
        print('All people are dead')
        break

    humans_on_world = count_humans(collected_humans)
    healthy_humans = humans_on_world.get(-1)
    sick_humans = humans_on_world.get(1)
    time_line.update({idx: [healthy_humans + sick_humans, sick_humans]})
    overview = time_sick_correlation(time_line)

    for human in _get_random_humans(grid):
        x, y = human
        m_x = rnd.randint(-1, 1)
        m_y = rnd.randint(-1, 1)
        if grid[x, y]:
            grid = grid[x, y].move(m_x, m_y, grid)
    update_humans(grid, TIME_RANGE)
    grid = update_grid(grid)

    if idx % 10 == 0:
        sns.heatmap(collected_humans, linewidth=0.5, cbar=False, ax=axs[0], cmap=sns.diverging_palette(220, 20, as_cmap=True), center=0)
        sns.lineplot(x='time_step', y='value', hue='variable', data=pd.melt(overview, ['time_step']), legend=False, ax=axs[1])

        fig.canvas.draw()

        plt.pause(0.05)

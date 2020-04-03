import numpy as np

class World:
    def __init__(self, x_dim: int, y_dim: int):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.world_grid = np.empty((self.x_dim, self.y_dim), dtype=object)
        self.grid_to_array_vec = np.vectorize(self._grid_to_array)

    def _grid_to_array(self, val):
        if val:
            if val.is_sick:
                return 1
            else:
                return 0
        return 2


    def translate_world(self):
        return self.grid_to_array_vec(self.world_grid)
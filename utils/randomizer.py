import random as rnd


def create_chance(probability: float) -> bool:
    reverse_probability = 1 - probability
    return rnd.choices(population=[[True], [False]], weights=[probability, reverse_probability])[0][0]

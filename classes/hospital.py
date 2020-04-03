import numpy as np
from .human import Doctor, Human


class Hospital:
    def __init__(self, pos_x: int, pos_y: int, capacity: int, staff_skill: int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.beds = np.empty((capacity,), dtype=object)
        self.doctor = Doctor(self.pos_x, self.pos_y, False, staff_skill)
        self.healing_chance = self.doctor.skill / 100

    def _get_free_bed(self):
        free_beds = np.where(self.beds == None)[0]
        if not free_beds.size:
            return None
        index = np.random.choice(free_beds.shape[0], 1, replace=False) 
        return free_beds[index][0]

    def accommodate_patient(self, patient: Human):
        free_bed = self._get_free_bed()
        if free_bed:
            self.beds[free_bed] = patient
            patient.pos_x, patient.pos_y = self.pos_x, self.pos_y
            patient.chance_to_cure =+ self.healing_chance
            return True

        return False

    def update(self):
        if self.doctor.is_sick:
            self.healing_chance = 0
        if not self.doctor.is_sick:
            self.healing_chance = self.doctor.skill / 100


    

    
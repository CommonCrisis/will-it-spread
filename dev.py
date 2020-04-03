from classes.hospital import Hospital
from classes.human import Human

hospital = Hospital(1, 1, 10, 8)

peter = Human(10, 5, True)
print(peter)
hospital.accommodate_patient(peter)

print(peter)
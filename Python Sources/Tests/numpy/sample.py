import random

def sample (a, b, year, computer_science, physical_science):
    a = 1970
    b = 2012
    year = [i for i in range(b-a)]
    for n in range (b-a):
        computer_science = random.sample(range(1, 100), (b-a))
        physical_science = random.sample(range(1, 100), (b-a))
        print (computer_science)
        print ('--------------------------------------------')
        print (physical_science)
    return a, b, year, computer_science, physical_science


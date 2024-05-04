import random

def foo(x, y, z):
    return 6*x**3 + 9*y**2 + 90*z - 25

def fitness(x, y, z):
    ans = foo(x, y, z)

    if ans < 0:
        return 99999
    else:
        return abs(1/ans)

solutions = []
RANDOM_COUNT = 10000
for s in range(1000):
    x = random.uniform(0, RANDOM_COUNT)
    y = random.uniform(0, RANDOM_COUNT)
    z = random.uniform(0, RANDOM_COUNT)
    solutions.append((x, y, z, fitness(x, y, z)))

for i in range(10000):
    rankedSolutions = []
    for s in solutions:
        rankedSolutions.append((fitness(s[0], s[1], s[2]), s))
    rankedSolutions.sort()
    rankedSolutions.reverse()

    print(f"==== Gen {i} best solutions === ")
    print(rankedSolutions[0])
    
    bestsolutions = rankedSolutions[:100]

    elements = []
    for s in bestsolutions:
        elements.append(s[1][0])
        elements.append(s[1][1])
        elements.append(s[1][2])

    newGen = []
    for _ in range(1000):
        x = random.choice(elements) * random.uniform(0.9, 1.01)
        y = random.choice(elements) * random.uniform(0.9, 1.01)
        z = random.choice(elements) * random.uniform(0.9, 1.01)
        newGen.append((x, y, z))
    
    solutions = newGen



print(solutions[:5])





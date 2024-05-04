# G Theory

The idea in this case would be more of ecology simulation rather than the genetic simulation. (kind of thoguh)
As it describes after how many simulations what takes into place. (No mutation nor crossover just an effective create offspring approach depending on the faceoffs.)


## Pseudocode 

Key Problems (changes from DEAP Examples)

- The fitness evaluation is really calculated when two individuals face each other.
- The count of children is not fixed, but depends on the 'fitness' resulting from the faceoff event. 
- The plot of the results change, it no longer matters the fitness but the type of dominant strategy.
- Mutation works as follows: 01010101 -> Then the strategy is determined as follows: majority(gen) == 0 => COOPERATE, else DEFECT


**Does it make sense to have a hof?**
- Hof should record the following instead:
- the number of cooperators. -> Records
- the number of defectors. -> Records
- hof: the total size of the population. (The objective is to increase as much as possible)



```python title="Modified selection"

def gambiteval(ind1, ind2):
    """
    Fitness is evaluated in this case when two individuals face each other.
    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoZTbudsbpcG_COpZ-JYNcwpFwVOXz8OyawhO6Vw-7&s
    """
    if ind1.strategy == "COOPERATIVE" and ind2.strategy == "AGGRESIVE":
        return (0, 3)
    elif ind1.strategy == "AGGRESIVE" and ind2.strategy == "COOPERATIVE":
        return (3, 0)
    elif ind1.strategy == "COOPERATIVE" and ind2.strategy == "COOPERATIVE":
        return (2, 2)
    elif ind1.strategy == "AGGRESIVE" and ind2.strategy == "AGGRESIVE":
        return (1, 1)
    else:
        return (0, 0)


def determineStrategy(individual):
    """
    The strategy is determined by the majority of the genes.
    - if majorty(gen) == 0 => COOPERATE
    - else DEFECT
    """
    count1 = sum([1 for i in individual if i == 1])
    count0 = sum([1 for i in individual if i == 0])
    if count1 > count0:
        return "AGGRESIVE"
    else:
        return "COOPERATIVE"
    

def selTournamentGambit(individuals, fit_attr="fitness"):
    """Select the best individual among 2 randomly chosen
    individuals, *k* times. The list returned contains
    references to the input *individuals*.

    # TODO
    - Make it so that they ALL have to face at least once someone (so it has to be a pair of individuals. if they cant find food, they are not selected (no cases could be random))

    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param tournsize: The number of individuals participating in each tournament.
    :param fit_attr: The attribute of individuals to use as selection criterion
    :returns: A list of offspirngs NOT the selected individuals.

    """
    chosen = []
    # randomize individuals
    random.shuffle(individuals)

    for i in range(individuals, 2):
        individual1 = individuals[i]
        individual2 = individuals[i+1]
        
        strategyInd1 = determineStrategy(individual1)
        strategyInd2 = determineStrategy(individual2)

        fitnessInd1Inc, fitnessInd2Inc = gambiteval(strategyInd1, strategyInd2)

        # Increase the fitness of the individuals.
        individual1.fitness.values[0] = fitnessInd1Inc
        individual2.fitness.values[0] = fitnessInd2Inc       
        
        # Add all the individuals evaluated to the population to have offspring.
        chosen.append(individual1, individual2)

    return chosen



# Modified varAnd()
def fitreproduceVarAnd(population, toolbox, cxpb, mutb):
    """
    The selected offspring, depends on the parents fitness. Thus clone depending on the fitness.

    """
    # 
    offspring = [] 
    for i in range(len(population)): # 0, 1, 2, 3, ...
        # append the right offspring.
        for fitnessIdx in range(population[i].fitness.values[0]): # 0, 1, 2, 3, ...
            offspring.append(toolbox.clone(population[i])) # Clone the individual and append it to the offspring.
    
    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):# 1, 3, 5, ... (Always has one before.)
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                          offspring[i]) # Run the assigned mate operation. And since it returns a pair, it should be assigned to a pair.
            del offspring[i - 1].fitness.values, offspring[i].fitness.values # Delete the fitness values of the offspring. (To be recalculated later)
        
    for i in range(len(offspring)): # 0, 1, 2, 3, ...
        if random.random() < mutpb: # If the random number is less than the mutation probability.
            offspring[i], = toolbox.mutate(offspring[i]) # Run the assigned mutate operation.
            del offspring[i].fitness.values # Delete the fitness values of the offspring. (To be recalculated later)

    return offspring

```


```python
    maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

    # plot statistics:
    sns.set_style("whitegrid")
    plt.plot(maxFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Max / Average Fitness')
    plt.title('Max and Average fitness over Generations')
    plt.show()
```

Charting requires the following modification:

- It should have a multi linechart trackin:
- Total population
- Number of cooperators
- Number of defectors
- on the axis:
  - x: number of generations
  - y: number of individuals


```python

# logbook.header = ['gen', 'population', 'coop_pop', 'defect_pop'] 
population, coop_pop, defect_pop = logbook.select("population", "coop_pop", "defect_pop")

# plot statistics:
sns.set_style("whitegrid")
plt.plot(population, color='blue')
plt.plot(coop_pop, color='green')
plt.plot(defect_pop, color='red')
plt.xlabel('Generation')
plt.ylabel('Population')
plt.title('Population over Generations')
plt.show()

```


select using tournament inspired faceoffs.


```python title="original selection"
def selTournament(individuals, k, tournsize, fit_attr="fitness"):
    """Select the best individual among *tournsize* randomly chosen
    individuals, *k* times. The list returned contains
    references to the input *individuals*.

    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param tournsize: The number of individuals participating in each tournament.
    :param fit_attr: The attribute of individuals to use as selection criterion
    :returns: A list of selected individuals.

    This function uses the :func:`~random.choice` function from the python base
    :mod:`random` module.
    """
    chosen = []
    for i in range(k):
        aspirants = selRandom(individuals, tournsize)
        chosen.append(max(aspirants, key=attrgetter(fit_attr)))
    return chosen
```



### Questions

- Can I solve the fitness problem from the tools available at the DEAP Library?
Here some variants that might require channging:

```

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
```

To something like

```
creator.create("Fitnessfaceoff", base.Fitness, weights=(1.0,))
```

**How varAnd works?**

```python
offspring = toolbox.select(population, len(population) - hof_size)

# Vary the pool of individuals
offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

# ... var and method



def varAnd(population, toolbox, cxpb, mutpb):
    r"""Part of an evolutionary algorithm applying only the variation part
    (crossover **and** mutation). The modified individuals have their
    fitness invalidated. The individuals are cloned so returned population is
    independent of the input population.

    https://deap.readthedocs.io/en/master/api/algo.html?highlight=varAnd#deap.algorithms.varAnd
    """
    # Copy each individual. Using the toolbox.clone method is better than
    offspring = [toolbox.clone(ind) for ind in population]

    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):# 1, 3, 5, ... (Always has one before.)
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                          offspring[i]) # Run the assigned mate operation. And since it returns a pair, it should be assigned to a pair.
            del offspring[i - 1].fitness.values, offspring[i].fitness.values # Delete the fitness values of the offspring. (To be recalculated later)

    for i in range(len(offspring)): # 0, 1, 2, 3, ...
        if random.random() < mutpb: # If the random number is less than the mutation probability.
            offspring[i], = toolbox.mutate(offspring[i]) # Run the assigned mutate operation.
            del offspring[i].fitness.values # Delete the fitness values of the offspring. (To be recalculated later)
    """
    Not how the mutated and mated population is the same count as the original population.
    """

    return offspring

```



### Review cases:

**Ant Evaluator Function**

he evaluation function use an instance of a simulator class to evaluate the individual. Each individual is given 600 moves on the simulator map (obtained from an external file). The fitness of each individual corresponds to the number of pieces of food picked up. In this example, we are using a classical trail, the Santa Fe trail, in which there is 89 pieces of food. Therefore, a perfect individual would achieve a fitness of 89.

https://deap.readthedocs.io/en/master/examples/gp_ant.html?highlight=fitness#evaluation-function
```
def evalArtificialAnt(individual):
    # Transform the tree expression to functional Python code
    routine = gp.compile(individual, pset)
    # Run the generated routine
    ant.run(routine)
    return ant.eaten,
```

Here we can see an case where tis is givenen a movement. But this approach is not what we should look for.

**Cooperative Coevolution**

This example explores cooperative coevolution using DEAP. This tutorial is not as complete as previous examples concerning type creation and other basic stuff. Instead, we cover the concepts of coevolution as they would be applied in DEAP. Assume that if a function from the toolbox is used, it has been properly registered. This example makes a great template for implementing your own coevolutionary algorithm, it is based on the description of cooperative coevolution by [Potter2001].

https://deap.readthedocs.io/en/master/examples/coev_coop.html?highlight=cooperative


```python
def evaluate(individuals):
    # Compute the collaboration fitness
    return fitness,

    while g < ngen:
        # Initialize a container for the next generation representatives
        next_repr = [None] * len(species)
        for (i, s), j in zip(enumerate(species), species_index):
            # Vary the species individuals
            s = algorithms.varAnd(s, toolbox, 0.6, 1.0)

            # Get the representatives excluding the current species
            r = representatives[:i] + representatives[i+1:]
            for ind in s:
                # Evaluate and set the individual fitness
                ind.fitness.values = toolbox.evaluate([ind] + r, target_set)

            # Select the individuals
            species[i] = toolbox.select(s, len(s))  # Tournament selection
            next_repr[i] = toolbox.get_best(s)[0]   # Best selection

        representatives = next_repr


```





## Setting Enhancements

Feature: Allowsing gambit selection


1. You need to separate the vairables to allow such as a method instead.
```python


```



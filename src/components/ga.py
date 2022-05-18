from numpy.random import randn
from random import choices, randint, uniform, shuffle
from dataclasses import dataclass, field
from typing import List
from copy import deepcopy

"""
Mutation threshold.
For each fractal a random number from an uniform distribution it's generated.
If random number < MUTATION_P --> mute the fractal
Otherwise --> don't mute the fractal
"""
MUTATION_P = 0.5 

@dataclass
class Fractal:
    """
    This class describes the structure of a fractal object 
    :param transformations: list of transformations of the fractal object, a transformation consist of a list of 8 real values
    :param score: the fitness of the fractal object
    """
    transformations: List[List[float]] = field(default_factory=list)
    score: int = 0

    def setScore(self, newScore):
        self.score = newScore
    
    # Function that mutates a fractal
    def mutate(self):
        for i in range(len(self.transformations)):
            for j in range(len(self.transformations[i])):
                # mutate each value of each transformation of the fractal
                self.transformations[i][j] = self.transformations[i][j] + (0.1 * randn())
    
    # Function that returns a new fractal object with the same parameters of the original one
    def copy(self):
        return Fractal(transformations=deepcopy(self.transformations), score=self.score)
    
    # Function that performs the cross-over on a list of parents (2 <= number of parents <= 4)
    """
    :param parents: list of parents
    :param n_genes: number of genes of the offspring
    :return offspring: return a new Fractal object obtained from the crossover operation
    """
    @classmethod
    def cross_over(cls, parents, n_genes):
        t_x_parent = [] # list with one transformation from each parent
        transformations = [] # list with all the transformations of all the parents minus the ones contained in t_x_parent
        for p in parents:
            shuffled = p.copy()
            shuffle(shuffled.transformations)
            for i, t in enumerate(shuffled.transformations):
                if i == 0:
                    t_x_parent.append(t.copy())
                else:
                    transformations.append(t.copy())
        length = len(transformations)
        weights = [1/length for _ in range(length)]
        
        # transformations of the offspring: they are determined by t_x_parent and (n_genes - |t_x_parent| ) transformations picked randomly from the transformations list
        return cls(t_x_parent + choices(transformations,weights, k= n_genes - len(parents))) 
    
    



# Evolution function that performs the evolution of the current population to generate a new generation of offspring
"""
:param population: vector of Fractal objects
:return final_pop: vector that contains the new offspring
"""
def evolve(population: List[Fractal]):
    # list that will contains the individuals of the original population and the mutated individuals
    mutated_pop = []     
    
    for fractal in population:
        # add the original individual to the mutated population
        mutated_pop.append(fractal.copy())  
        
        if uniform(0, 1) < MUTATION_P:
            fractal.mutate()
            # add the mutated individual to the mutated population
            mutated_pop.append(fractal.copy()) 
    
    # Extraction of the probability of being selected as a parent for each individual in the population (fitness-proportionate selection)        
    total_fitness = sum([f.score for f in mutated_pop])
    
    # list that contains for each individual of the populations its probability to be chosen as a parent
    prob_sel = [f.score/total_fitness for f in mutated_pop] 
    
    # Creation of the offspring population using mutation and crossover
    final_pop = [] 
    for _ in range(len(population) - 3):
        # determine the number of parents for an offspring
        n_parents = randint(2, 4) 

        # select n_parents from mutated_pop. Each parent is selected accordingly to prob_sel
        parents = choices(mutated_pop, weights=prob_sel, k=n_parents)  

        # determine the number of genes for the offspring. It is selected as a random number between the number of parents and the maximal length of the genome between the parents
        max_genes = max([len(fract.transformations) for fract in parents])
        if(max_genes!=n_parents):
            n_genes = randint(n_parents, max_genes)
        else:
            n_genes = n_parents       
        
        final_pop.append(Fractal.cross_over(parents, n_genes))
    
    # sort the initial population according to the score of each fractal 
    population.sort(key = lambda x: x.score)
    
    # add the elite individuals to the individuals obtained from mutation and cross-over. The elite individuals are selected as the three individuals of the populations that has the higher score
    final_pop += population[:3]
    
    return final_pop 











    
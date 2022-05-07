from cgi import parse_multipart
from secrets import choice
import numpy as np
from random import choices, randint, uniform


from dataclasses import dataclass, field
from typing import List
from copy import deepcopy

@dataclass()
class Fractal:
    transformations: List[List[float]] = field(default_factory=list)
    score: int = 0
    
    def mutate(self):
        for i in range(len(self.transformations)):
            for j in range(len(self.transformations[i])):
                self.transformations[i][j] = self.transformations[i][j] + (0.1 * np.random.randn())
    
    def copy(self):
        return Fractal(transformations=deepcopy(self.transformations), score=self.score)
    
    @classmethod
    def cross_over(cls, parents, n_genes):
        transformations = []
        for p in parents:
            for t in p.transformations:
                transformations.append(t.copy())
        length = len(transformations)
        weights = [1/length for _ in range(length)]
        return cls(choices(transformations,weights, k= n_genes))
    
    

def evolutionV2(population: List[Fractal]):
    mutated_pop = [] 
    for fractal in population:
        mutated_pop.append(fractal.copy())
        if uniform(0, 1) < MUTATION_P:
            fractal.mutate()
            mutated_pop.append(fractal.copy())
    total_fitness = sum([f.score for f in mutated_pop])
    prob_sel = [f.score/total_fitness for f in mutated_pop]
    final_pop = [] 
    for _ in range(len(population) - 3):
        n_parents = randint(2, 4) 
        parents = choices(mutated_pop, weights=prob_sel, k=n_parents) 
        n_genes = max([len(fract.transformations) for fract in parents])
        final_pop.append(Fractal.cross_over(parents, n_genes))
    population.sort(key = lambda x: x.score)
    return final_pop + population[:3]

"""
Mutation threshold.
For each fractal a random number from an uniform distribution it's generated.
If random number < MUTATION_P --> mute the fractal
Otherwise --> don't mute the fractal
"""
MUTATION_P = 0.5 


# Function that mutates a fractal
"""
:param fract: fractal is the list of transformations of a fractal in the population
"""
def mutate_fract(fract):
    for i in range(len(fract)):
        for j in range(len(fract[i])):
            fract[i][j] = fract[i][j] + (0.1 * np.random.randn()) # mutate each value of each transformation of the fractal


# Function that performs the cross-over on a list of parents (2 <= number of parents <= 4)
"""
:param parents: list of parents. For each parent it contains the parent's transformations
:param n_genes: number of genes of the offspring
:return offspring: tuple containing the trasformations of the offspring (offspring's genome)
"""
def cross_over(parents, n_genes):
    offspring = [] # list that contains the transformations of the offspring
    n = 0

    while n_genes > 0:
        for i in range(len(parents)):
            print("parent iterator = " , i)
            print("parent = ", parents )
            if (n <= len(parents[i])):
                gene = choice(parents[i]) # extract randomly a gene from the parent. These gene will be part of the offspring's genome
                parents[i].remove(gene) # remove the gene from the parent. In this way we cannot select these gene multiple time for the offspring's genome
                offspring.append(gene)
                n_genes -= 1
            print("n_genes = " + str(n_genes))
        n += 1

    return offspring


# Evolution function that performs the evolution of the current population to generate a new generation of offspring
"""
:param pop_with_eval: vector that contains for each individual of the population its transformations and its evaluation given by the user
:return final_pop: vector that contains the new offspring. For each offspring it contains the correspondding transformations.
"""
def evolution(pop_with_eval):

    # Mutation
    mutated_pop = [] # list that will contains the individuals of the original population and the mutated individuals
    for fractal, score in pop_with_eval:
        mutated_pop.append((fractal, score)) # add the original individual to the mutated population
        if uniform(0, 1) < MUTATION_P:
            mutate_fract(fractal)
            mutated_pop.append((fractal, score)) # add the mutated individual to the mutated population


    # Extraction of the probability of being selected as a parent for each individual in the population (fitness-proportionate selection)
    prob_sel = [] # list that contains for each individual of the populations its probability to be chosen as a parent
    total_fitness = sum([score for _, score in mutated_pop])
    for _, score in mutated_pop:
        prob_sel.append(score/total_fitness)

    # Creation of the offspring population using mutation and crossover
    final_pop = [] # list that contains the offspring generated from the current population (pop_with_eval). The number of offspring is the same number of individuals of the current population
    for _ in range(len(pop_with_eval) - 3):
        n_parents = randint(2, 4) # determine the number of parents for an offspring
        parents = choices(mutated_pop, weights= prob_sel, k = n_parents) # select n_parents from mutated_pop. Each parent is selected accordingly to prob_sel
        
        maxi = max([len(fract) for fract , _ in parents])
        if(n_parents == maxi):
            n_genes = n_parents
        elif(n_parents > maxi):
             n_genes = randint(maxi, n_parents) # determine the number of genes for the offspring. It is selected as a random number between the number of parents and the maximal length of the genome between the parents
        elif(n_parents < maxi):
            n_genes = randint(n_parents, maxi) # determine the number of genes for the offspring. It is selected as a random number between the number of parents and the maximal length of the genome between the parents
        final_pop.append(cross_over([par for par, _ in parents], n_genes)) # generate a new offspring

    pop_with_eval.sort(key = lambda x: x[1], reverse = True)
    elite = pop_with_eval[:3] # extract the elite individuals from the current population (pop_with_eval). The elite individuals are selected as the three individuals of the populations that has the higher score

    for e,_ in elite:
        final_pop.append(e)
    #final_pop = final_pop + elite # add the elite individuals to the individuals obtained from mutation and cross-over

    return final_pop


def main():
    fake_fractals : List[Fractal]= []
    for i in range(5):
        fract = Fractal()
        for _ in range(5):
            fract.transformations.append([float(i) for _ in range(7)])
        fract.score = i
        fake_fractals.append(fract)
    
    
    evolved =  evolutionV2(fake_fractals)
    
   
    

if __name__ == "__main__":
    main()
    
import numpy.random as npr
import random
from genetic import CHROMOSOME_SIZE, random_gene, random_chromosome


def mutate(chromosome):
    mutate_point = random.randint(0, CHROMOSOME_SIZE - 1)
    mutation = chromosome[:mutate_point] + random_gene() + chromosome[mutate_point + 1:]
    return mutation

ch = random_chromosome()
print(ch)
mt = mutate(ch)
print(mt)
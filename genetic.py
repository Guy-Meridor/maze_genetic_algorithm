from maze.maze import Maze, DIRECTIONS_SIGNS
import random
import numpy.random as npr
import math

MAZE_SIZE = 50
GENERATIONS_NUM = 1000
POPULATION_IN_GENERATION = 50
OBSTACLES = False
CHROMOSOME_SIZE = MAZE_SIZE ** 2 if OBSTACLES else 2 * (MAZE_SIZE - 1)
REPEAT_COST = 10
DISTANCE_LEFT_EXPONENTIAL = 2
UNSOLVED_COST = 100

# Generic params
ELITE_PCT = 0.05
ELITE_COUNT = round(POPULATION_IN_GENERATION * ELITE_PCT)
MUTATE_PCT = 0.1
CROSSOVER_PCT = 0.95


class genetic_runner:
    def __init__(self):
        self.create_maze(MAZE_SIZE)

    def create_maze(self, size):
        # start = (random.randint(0, size), random.randint(0, size))
        start = (size - 1, size - 1)
        # destination = (random.randint(0, size), random.randint(0, size))
        destination = (5, 5)
        self.maze = Maze(size=size, start=start, destination=destination)

    def run(self):
        result = self.run_generations()
        return result

    def fitness_value(self, chromosome):
        stats = self.maze.walk_maze(chromosome)
        cost = stats.steps + \
               REPEAT_COST * stats.repeats + \
               stats.disFromDest ** DISTANCE_LEFT_EXPONENTIAL + \
               (UNSOLVED_COST if not stats.solved else 0)

        return 1 / cost

    def crossover(self, p1, p2):
        crossover_point = random.randint(0, CHROMOSOME_SIZE)
        return (p1[:crossover_point] + p2[crossover_point:],
                p2[:crossover_point] + p1[crossover_point:])

    def mutate(self, chromosome):
        mutate_point = random.randint(0, CHROMOSOME_SIZE - 1)
        mutation = chromosome[:mutate_point] + random_gene() + chromosome[mutate_point + 1:]
        return mutation

    def generate_generation(self, population):

        fitness_array = [self.fitness_value(chromosome) for chromosome in population]
        total_fitness = sum(fitness_array)
        roulette_array = [fitness / total_fitness for fitness in fitness_array]

        next_population = population[:ELITE_COUNT]
        population_to_create = POPULATION_IN_GENERATION - ELITE_COUNT
        for i in range(math.ceil(population_to_create / 2)):
            c1, c2 = npr.choice(population, 2, p=roulette_array)
            if random.random() < CROSSOVER_PCT:
                c1, c2 = self.crossover(c1, c2)

            if random.random() < MUTATE_PCT:
                c1, c2 = self.mutate(c1), self.mutate(c2)

            next_population.extend([c1, c2])

        next_population.sort(key=lambda x: self.fitness_value(x), reverse=True)
        return next_population

    def run_generations(self):
        population = self.initiate_population()
        self.data_tracking(population)

        for generation in range(GENERATIONS_NUM):
            population = self.generate_generation(population)
            self.data_tracking(population)

        return population[0]

    def initiate_population(self):
        population = random_population()
        population.sort(key=lambda x: self.fitness_value(x), reverse=True)
        return population

    def data_tracking(self, generation):
        print(generation[0])


random_gene = lambda: random.choice(DIRECTIONS_SIGNS)

random_chromosome = lambda: "".join([random_gene() for i in range(CHROMOSOME_SIZE)])

random_population = lambda: [random_chromosome() for i in range(POPULATION_IN_GENERATION)]

if __name__ == "__main__":
    runner = genetic_runner()
    result = runner.run()
    print(result)

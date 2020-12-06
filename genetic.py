from maze.maze import Maze, DIRECTIONS_SIGNS, distance
import random
import numpy.random as npr
import matplotlib.pyplot as plt

MAZE_SIZE = 100
GENERATIONS_NUM = 1000
POPULATION_IN_GENERATION = 50
OBSTACLES = 400
CHROMOSOME_SIZE = 2 * (MAZE_SIZE - 1)
REPEAT_COST = 5
STEP_COST = 5
DISTANCE_LEFT_EXPONENTIAL = 2
UNSOLVED_COST = 100

# Generic params
ELITE_PCT = 0.1
ELITE_COUNT = round(POPULATION_IN_GENERATION * ELITE_PCT)
MUTATE_PCT = 0.2
CROSSOVER_PCT = 0.95
CONVERGENCE_GENERATIONS = 100

class genetic_runner:
    def __init__(self, size, num_of_obstacles=0):
        self.num_of_obstacles = num_of_obstacles
        self.size = size
        self.create_maze()
        self.generation_min = []
        self.generation_avg = []
        self.generation_max = []
        self.fitness_dict = {}

    def create_maze(self):
        allPoints = [(x, y) for x in range(self.size) for y in range(self.size)]
        sampled = random.sample(allPoints, self.num_of_obstacles + 2)
        start = sampled[0]
        destination = sampled[1]
        obstacles = sampled[2:]

        self.maze = Maze(size=self.size, start=start, destination=destination, obstacles=obstacles)

    def run(self):
        result = self.run_generations()
        return result

    def fitness_value(self, chromosome):
        stats = self.maze.walk_maze(chromosome)[0]
        cost = stats.steps * STEP_COST + \
               REPEAT_COST * stats.repeats + \
               stats.disFromDest ** DISTANCE_LEFT_EXPONENTIAL + \
               (0 if stats.disFromDest == 0 else UNSOLVED_COST)

        return 1 / cost

    def crossover(self, p1, p2):
        crossover_point = random.randint(0, CHROMOSOME_SIZE)
        return (p1[:crossover_point] + p2[crossover_point:],
                p2[:crossover_point] + p1[crossover_point:])

    def mutate(self, chromosome):
        mutate_point = random.randint(0, CHROMOSOME_SIZE - 1)
        mutation = chromosome[:mutate_point] + random_gene() + chromosome[mutate_point + 1:]
        return mutation

    def generate_generation(self, population, fitness_array):
        total_fitness = sum(fitness_array)
        roulette_array = [fitness / total_fitness for fitness in fitness_array]
        next_population = population[:ELITE_COUNT]

        while len(next_population) < POPULATION_IN_GENERATION:
            c1, c2 = npr.choice(population, 2, p=roulette_array)
            if random.random() < CROSSOVER_PCT:
                c1, c2 = self.crossover(c1, c2)

            if random.random() < MUTATE_PCT:
                c1, c2 = self.mutate(c1), self.mutate(c2)

            next_population.extend([c1, c2])

        # next_population, next_fitness_array = self.create_fitness_array_and_sort_population(population)
        self.update_fitness_dict(next_population)
        next_population.sort(key=lambda x: self.fitness_dict[x], reverse=True)
        next_fitness_array = [self.fitness_dict[x] for x in next_population]
        return (next_population, next_fitness_array)

    def run_generations(self):
        population, fitness_array = self.initiate_population()
        self.data_tracking(population, fitness_array)

        for generation in range(GENERATIONS_NUM):
            population, fitness_array = self.generate_generation(population, fitness_array)
            self.data_tracking(population, fitness_array)

            if self.check_if_convergence():
                break

        return population[0]

    def check_if_convergence(self):
        if len(self.generation_max) <= CONVERGENCE_GENERATIONS:
            return False
        else:
            last_generations_max = self.generation_max[-CONVERGENCE_GENERATIONS:]
            firstMax = last_generations_max[0]
            for mx in last_generations_max:
                if mx != firstMax:
                    return False

            return True


    def initiate_population(self):
        population = random_population()
        self.update_fitness_dict(population)
        fitness_array = [self.fitness_dict[x] for x in population]
        return (population, fitness_array)

    def data_tracking(self, generation, fitness_array):
        print(generation[0])
        self.generation_max.append(fitness_array[0])
        self.generation_avg.append(avg(fitness_array))
        self.generation_min.append(fitness_array[POPULATION_IN_GENERATION - 1])

    def update_fitness_dict(self, population):
        for chromosome in population:
            if chromosome not in self.fitness_dict:
                self.fitness_dict[chromosome] = self.fitness_value(chromosome)


    def showGraphs(self):
        # plotting the line 1 points
        plt.plot(self.generation_min, label="minimum fitness")
        plt.plot(self.generation_avg, label="average fitness")
        plt.plot(self.generation_max, label="maximum fitness")
        plt.xlabel('x - generation number')
        plt.ylabel('y - fitness')
        plt.title('fitness of chromosomes in {} generations'.format(GENERATIONS_NUM))
        plt.legend()
        plt.figure()


random_gene = lambda: random.choice(DIRECTIONS_SIGNS)

random_chromosome = lambda: "".join([random_gene() for i in range(CHROMOSOME_SIZE)])

random_population = lambda: [random_chromosome() for i in range(POPULATION_IN_GENERATION)]

avg = lambda arr: sum(arr) / len(arr)




def list_intersects(a, b):
    a_set = set(a)
    b_set = set(b)
    return len(a_set.intersection(b_set)) > 0


if __name__ == "__main__":
    runner = genetic_runner(MAZE_SIZE, OBSTACLES)
    result = runner.run()

    distance = distance(runner.maze.startPoint, runner.maze.destinationPoint) * STEP_COST
    print(runner.maze.startPoint, runner.maze.destinationPoint,
          distance, 1 / distance)
    print(result)
    print(runner.fitness_value(result))
    runner.showGraphs()
    runner.maze.drawPath(result)

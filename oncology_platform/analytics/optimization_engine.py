import random
from oncology_platform.analytics.codex_metrics import CodexScout

class OptimizationCandidate:
    """Represents a potential therapeutic combination candidate for optimization."""
    def __init__(self, gravity: float, breadth: float, pace: float, resistance: float, position=None):
        self.gravity = gravity
        self.breadth = breadth
        self.pace = pace
        self.resistance = resistance
        self.position = position if position is not None else [gravity, breadth, pace, resistance]

class GeneticCoach:
    """
    Uses Genetic Algorithms (GA) to evolve therapeutic candidates.
    Logic based on Genetic Algorithm optimization logic.
    """
    
    def __init__(self, population_size: int, mutation_rate: float):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population(population_size)

    def initialize_population(self, size: int):
        population = []
        for _ in range(size):
            # Generate random drug profiles
            candidate = OptimizationCandidate(
                gravity=random.uniform(1.0, 10.0),
                breadth=random.uniform(0.1, 1.0),
                pace=random.uniform(1.0, 10.0),
                resistance=random.uniform(1.0, 100.0)
            )
            population.append(candidate)
        return population

    def fitness_function(self, candidate: OptimizationCandidate) -> float:
        """
        Evaluates a candidate based on the Codex RO score.
        Candidates with RO > 1.0 are prioritized.
        """
        scout = CodexScout()
        return scout.calculate_RO(candidate.gravity, candidate.breadth, candidate.pace, candidate.resistance)

    def select_best_players(self, population):
        """Perform tournament selection or roulette wheel selection."""
        # Rank by fitness
        sorted_pop = sorted(population, key=self.fitness_function, reverse=True)
        # Select top 50%
        return sorted_pop[:max(2, len(sorted_pop) // 2)]

    def crossover(self, parents):
        offspring = []
        while len(offspring) < self.population_size:
            p1 = random.choice(parents)
            p2 = random.choice(parents)
            
            # Blend crossover
            alpha = random.random()
            gravity = alpha * p1.gravity + (1 - alpha) * p2.gravity
            breadth = alpha * p1.breadth + (1 - alpha) * p2.breadth
            pace = alpha * p1.pace + (1 - alpha) * p2.pace
            resistance = alpha * p1.resistance + (1 - alpha) * p2.resistance
            
            offspring.append(OptimizationCandidate(gravity, breadth, pace, resistance))
        return offspring

    def mutate(self, offspring):
        for candidate in offspring:
            if random.random() < self.mutation_rate:
                candidate.gravity = max(0.1, candidate.gravity + random.normalvariate(0, 1))
            if random.random() < self.mutation_rate:
                candidate.breadth = max(0.01, min(1.0, candidate.breadth + random.normalvariate(0, 0.1)))
            if random.random() < self.mutation_rate:
                candidate.pace = max(0.1, candidate.pace + random.normalvariate(0, 1))
            if random.random() < self.mutation_rate:
                candidate.resistance = max(1.0, candidate.resistance + random.normalvariate(0, 5))
        return offspring

    def evolve_roster(self, generations: int) -> OptimizationCandidate:
        """
        Iterative selection, crossover, and mutation.
        """
        for _ in range(generations):
            parents = self.select_best_players(self.population)
            offspring = self.crossover(parents)
            self.population = self.mutate(offspring)
            
        return self.get_mvp()

    def get_mvp(self) -> OptimizationCandidate:
        """Return the highest fitness candidate."""
        return max(self.population, key=self.fitness_function)

class WhaleOptimizer:
    """
    Uses Whale Optimization Algorithm (WOA) for 'Encircling' the disease target.
    Logic based on biological prey encircling heuristics.
    """
    
    def __init__(self, num_whales: int = 10, dim: int = 4):
        self.num_whales = num_whales
        self.dim = dim
        self.whales = []
        self.leader_position = None
        self.leader_score = -float('inf')
        self.init_whales()

    def init_whales(self):
        self.whales = []
        for _ in range(self.num_whales):
            # Pos representation: [gravity, breadth, pace, resistance]
            pos = [
                random.uniform(1.0, 10.0),
                random.uniform(0.1, 1.0),
                random.uniform(1.0, 10.0),
                random.uniform(10.0, 100.0)
            ]
            self.whales.append(pos)
        self.update_leader()

    def update_leader(self):
        scout = CodexScout()
        for whale in self.whales:
            score = scout.calculate_RO(whale[0], whale[1], whale[2], whale[3])
            if score > self.leader_score:
                self.leader_score = score
                self.leader_position = list(whale)

    def encircle_prey(self, a, C):
        for i in range(self.num_whales):
            for j in range(self.dim):
                r = random.random()
                A = 2 * a * r - a
                D_leader = abs(C * self.leader_position[j] - self.whales[i][j])
                self.whales[i][j] = max(0.1, self.leader_position[j] - A * D_leader)

    def bubble_net_attack(self, b, l):
        for i in range(self.num_whales):
            for j in range(self.dim):
                D_leader = abs(self.leader_position[j] - self.whales[i][j])
                # Spiral updating position
                self.whales[i][j] = max(0.1, D_leader * round(random.uniform(-1, 1), 4) * (b * l) + self.leader_position[j])

    def search_prey(self, a, C):
        for i in range(self.num_whales):
            rand_whale = random.choice(self.whales)
            for j in range(self.dim):
                r = random.random()
                A = 2 * a * r - a
                D_rand = abs(C * rand_whale[j] - self.whales[i][j])
                self.whales[i][j] = max(0.1, rand_whale[j] - A * D_rand)

    def hunt_target(self, max_iter: int) -> list:
        """
        Mimics bubble-net attacking strategy.
        """
        b = 1.0
        for it in range(max_iter):
            # Coefficient a decreases linearly from 2 to 0
            a = 2.0 - it * (2.0 / max_iter)
            
            for i in range(self.num_whales):
                r = random.random()
                C = 2 * r
                p = random.random()
                
                if p < 0.5:
                    if abs(a) < 1:
                        self.encircle_prey(a, C)
                    else:
                        self.search_prey(a, C)
                else:
                    l = random.uniform(-1, 1)
                    self.bubble_net_attack(b, l)
            
            self.update_leader()
            
        return self.leader_position

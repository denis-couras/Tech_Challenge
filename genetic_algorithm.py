import random
import math
import numpy as np
from typing import List, Tuple

WEIGHT_ICMS = 0.1      
WEIGHT_PERICULOSITY = 2
WEIGHT_TOLL = 1.5 
WEIGHT_TIME = 0.8 
WEIGHT_ROAD_CONDITIONS = 3

def calculate_fitness(route):
    total_distance = 0
    total_icms = 0
    total_periculosidade = 0
    total_pedagio = 0
    total_tempo = 0
    total_estrada_ruim = 0

    for i in range(len(route) - 1):
        cidade_atual = route[i]
        proxima_cidade = route[i + 1]

        distancia = np.linalg.norm(np.array(cidade_atual[:2]) - np.array(proxima_cidade[:2]))
        total_distance += distancia

        total_icms += cidade_atual[2]

        total_periculosidade += cidade_atual[3]

        if len(cidade_atual) > 4:
            total_pedagio += cidade_atual[4]

        velocidade_media = cidade_atual[5] if len(cidade_atual) > 5 else 80
        total_tempo += distancia / velocidade_media

        if len(cidade_atual) > 6:
            total_estrada_ruim += distancia * cidade_atual[6]

    fitness = (
        total_distance +
        (total_icms * WEIGHT_ICMS) +  # Ajuste do peso do ICMS
        (total_periculosidade * WEIGHT_PERICULOSITY) +  # Peso maior para periculosidade
        (total_pedagio * WEIGHT_TOLL) +  # Pedágios afetam o custo
        (total_tempo * WEIGHT_TIME) +  # Tempo de viagem importa, mas não tanto quanto distância
        (total_estrada_ruim * WEIGHT_ROAD_CONDITIONS)  # Estradas ruins impactam fortemente a rota
    )

    return fitness

def generate_random_population_v3(
    cities_location: List[Tuple[float, float]], 
    population_size: int, 
    city: Tuple[float, float]
) -> List[List[Tuple[float, float]]]:
    return [[city] + random.sample([c for c in cities_location if c != city], len(cities_location) - 1) 
            for _ in range(population_size)]

def generate_random_population(cities_location: List[Tuple[float, float]], population_size: int) -> List[List[Tuple[float, float]]]:
    return [random.sample(cities_location, len(cities_location)) for _ in range(population_size)]

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    return math.dist(point1, point2)

def order_crossover(parent1: List[Tuple[float, float]], parent2: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    length = len(parent1)

    start_index = random.randint(0, length - 2)
    end_index = random.randint(start_index + 1, length)

    child = [None] * length
    child[start_index:end_index] = parent1[start_index:end_index]

    used_genes = set(child[start_index:end_index])
    remaining_genes = [gene for gene in parent2 if gene not in used_genes]

    insert_index = 0
    for i in range(length):
        if child[i] is None:
            child[i] = remaining_genes[insert_index]
            insert_index += 1

    return child

def mutate(solution: List[Tuple[float, float]], mutation_probability: float) -> List[Tuple[float, float]]:
    if len(solution) < 2 or random.random() >= mutation_probability:
        return solution

    mutated_solution = solution[:] 
    index = random.randint(1, len(solution) - 2)
    mutated_solution[index], mutated_solution[index + 1] = mutated_solution[index + 1], mutated_solution[index]
    return mutated_solution

def sort_population(population: List[List[Tuple[float, float]]], fitness: List[float]) -> Tuple[List[List[Tuple[float, float]]], List[float]]:
    sorted_population, sorted_fitness = zip(*sorted(zip(population, fitness), key=lambda x: x[1]))
    return list(sorted_population), list(sorted_fitness)

def normalize_icms(icms_values: list[float]) -> list[float]:
    max_icms = max(icms_values)
    
    if max_icms == 0:
        return [0] * len(icms_values)
    
    normalized_icms = [icms / max_icms for icms in icms_values]
    return normalized_icms

def normalize_distances(distances: list[float]) -> list[float]:
    max_distance = max(distances)
    
    if max_distance == 0:
        return [0] * len(distances)
    
    normalized_distances = [distance / max_distance for distance in distances]
    return normalized_distances

def main():
    N_CITIES = 10
    POPULATION_SIZE = 100
    N_GENERATIONS = 100
    MUTATION_PROBABILITY = 0.3

    cities_locations = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(N_CITIES)]
    population = generate_random_population(cities_locations, POPULATION_SIZE)

    best_fitness_values = []
    best_solutions = []

    for generation in range(N_GENERATIONS):
        population_fitness = [calculate_fitness(individual) for individual in population]
        population, population_fitness = sort_population(population, population_fitness)

        best_fitness = population_fitness[0]
        best_solution = population[0]

        best_fitness_values.append(best_fitness)
        best_solutions.append(best_solution)

        print(f"Generation {generation}: Best fitness = {best_fitness}")
        new_population = [best_solution]

        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(population[:10], 2)
            child = order_crossover(parent1, parent2)
            child = mutate(child, MUTATION_PROBABILITY)
            new_population.append(child)

        population = new_population

if __name__ == '__main__':
    main()
    


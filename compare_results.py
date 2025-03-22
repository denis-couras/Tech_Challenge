import time
import numpy as np
from genetic_algorithm import calculate_fitness
from logistic_machine_learning import model, calculate_distance, cities
import torch

N_CITIES = 15
POPULATION_SIZE = 100
N_GENERATIONS = 100
MUTATION_PROBABILITY = 0.3

def run_genetic_algorithm():
    start_time = time.time()
    end_time = time.time()
    genetic_time = end_time - start_time
    return genetic_time

def run_machine_learning():
    start_time = time.time()
    state = cities.flatten()
    route = []
    visited = set()
    
    while len(route) < N_CITIES:
        state_tensor = torch.tensor(state, dtype=torch.float32)
        q_values = model(state_tensor)
        action = torch.argmax(q_values).item()
        
        if action in visited:
            continue
        
        visited.add(action)
        route.append(cities[action])
        
        next_state = np.zeros((N_CITIES, 2))
        next_state[:len(route)] = route
        state = next_state.flatten()
    
    ml_distance = calculate_distance(route)
    end_time = time.time()
    ml_time = end_time - start_time
    return ml_distance, ml_time

genetic_time = run_genetic_algorithm()
ml_distance, ml_time = run_machine_learning()

print(f"Tempo Algoritmo Genético: {genetic_time:.4f} segundos")
print(f"Tempo Machine Learning: {ml_time:.4f} segundos")
print(f"Distância total (ML - DQN): {ml_distance:.4f}")

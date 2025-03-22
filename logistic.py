import pygame
from pygame.locals import *
import random
import itertools
from genetic_algorithm import *
from draw_functions import *
import sys
import numpy as np
import pygame
from benchmark_attbrazil_capitals import *

# Define constant values
# pygame
NODE_RADIUS = 5
FPS = 30
PLOT_X_OFFSET = 550

# GA
N_CITIES = 15
POPULATION_SIZE = 500
N_GENERATIONS = None
MUTATION_PROBABILITY = 0.5

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (135, 206, 250) 

Y_OFFSET = 40
WIDTH, HEIGHT = 1200, 600
min_x = min(point[1][1] for point in capitals_data)
min_y = min(point[1][0] for point in capitals_data)

att_cities_locations = np.array([
    (point[1][1] - min_x, point[1][0] - min_y, point[2], point[3])  # Ajusta para um mínimo positivo
    for point in capitals_data
])

max_x = max(point[0] for point in att_cities_locations)
max_y = max(point[1] for point in att_cities_locations)

max_x = max(1, max_x)
max_y = max(1, max_y) 

scale_x = (WIDTH - PLOT_X_OFFSET - NODE_RADIUS) / max_x
scale_y = HEIGHT / max_y

scale_factor = 0.90

cities_locations = [
    (int(point[0] * scale_x * scale_factor + PLOT_X_OFFSET), 
     int(HEIGHT - point[1] * scale_y * scale_factor - Y_OFFSET), point[2], point[3])  # Subtrai para subir mais
    for point in att_cities_locations
]

target_solution = [cities_locations[i-1] for i in capitals_order]
fitness_target_solution = calculate_fitness(target_solution)
print(f"Best Solution: {fitness_target_solution}")

all_best_fitness = fitness_target_solution
all_best_solution = target_solution
fitness_history = {}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            exit()

def update_population(population, population_fitness):
    best_solution = population[0]
    new_population = [best_solution]

    fitness_sum = sum(1 / f if f > 0 else 1e-10 for f in population_fitness)
    probabilities = [(1 / f if f > 0 else 1e-10) / fitness_sum for f in population_fitness]

    while len(new_population) < POPULATION_SIZE:
        parent1, parent2 = random.choices(population, weights=probabilities, k=2)
        child = mutate(order_crossover(parent1, parent2), MUTATION_PROBABILITY)
        new_population.append(child)

    return new_population

def draw_screen(screen, best_fitness_values, cities_locations, best_solution, population, fitness_history, capital_name):
    screen.fill(WHITE)
    draw_plot(screen, list(range(len(best_fitness_values))), best_fitness_values, y_label="Fitness - Distancia")
    draw_cities(screen, cities_locations, YELLOW, NODE_RADIUS)
    draw_paths(screen, best_solution, LIGHT_BLUE, width=2)
    draw_paths(screen, population[1], rgb_color=(128, 128, 128), width=1)
    draw_plot_fitness(screen, fitness_history)
    print(f"Geração {len(best_fitness_values)}: Melhor fitness = {round(best_fitness_values[-1], 2)} for {capital_name}")
    pygame.display.flip()

pygame.display.set_caption("Logistic Solver using Pygame")
clock = pygame.time.Clock()

for city, capital in zip(cities_locations, capitals_data):
    generation_counter = itertools.count(start=1)
    population = generate_random_population_v3(cities_locations, POPULATION_SIZE, city)

    best_fitness_values = []
    best_solutions = []

    for generation in range(50):
        handle_events()
        population_fitness = [calculate_fitness(ind) for ind in population]
        population, population_fitness = zip(*sorted(zip(population, population_fitness), key=lambda x: x[1]))

        best_solution, best_fitness = population[0], population_fitness[0]
        best_fitness_values.append(best_fitness)
        best_solutions.append(best_solution)

        if best_fitness < all_best_fitness:
            all_best_fitness = best_fitness
            all_best_solution = best_solution

        fitness_history[capital[0]] = best_fitness   
        draw_screen(screen, best_fitness_values, cities_locations, best_solution, population, fitness_history, capital[0])

        population = update_population(population, population_fitness)
        clock.tick(FPS)

def handle_events():
    for event in pygame.event.get():
        if event.type in {pygame.QUIT, pygame.KEYDOWN} and (event.type != pygame.KEYDOWN or event.key == pygame.K_q):
            pygame.quit()
            exit()

def update_screen():
    screen.fill(WHITE)
    draw_plot(screen, range(len(best_fitness_values)), best_fitness_values, y_label="Fitness - Distance (pxls)")
    draw_cities(screen, cities_locations, YELLOW, NODE_RADIUS)
    draw_paths_with_arrow(screen, all_best_solution, BLUE, width=1)
    draw_plot_fitness(screen, fitness_history)
    pygame.display.flip()

while True:
    handle_events()
    update_screen()
    clock.tick(FPS)

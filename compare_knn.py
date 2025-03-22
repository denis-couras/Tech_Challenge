import random
import math
from benchmark_attbrazil_capitals import *

def calculate_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def calculate_cost(city1, city2):
    _, coord1, icms1, per1, ped1, vel1, quality1 = city1
    _, coord2, icms2, per2, ped2, vel2, quality2 = city2

    distance = calculate_distance(coord1, coord2)
    avg_icms = (icms1 + icms2) / 2
    avg_periculosidade = (per1 + per2) / 2
    avg_pedagio = (ped1 + ped2) / 2
    avg_velocidade = (vel1 + vel2) / 2
    avg_quality = (quality1 + quality2) / 2

    cost = (distance * 0.5) + (avg_icms * 0.2) + (avg_periculosidade * 0.2) + (avg_pedagio * 0.1) - (avg_quality * 0.3)

    return cost, distance

def nearest_neighbor(capitals):
    unvisited = capitals[:]
    start_city = random.choice(unvisited)
    unvisited.remove(start_city)

    route = [start_city]
    total_cost = 0
    total_distance = 0

    while unvisited:
        current_city = route[-1]
        next_city, min_distance = min(
            ((city, calculate_cost(current_city, city)) for city in unvisited),
            key=lambda x: x[1][0]
        )

        cost, distance = min_distance
        total_cost += cost
        total_distance += distance
        route.append(next_city)
        unvisited.remove(next_city)

    final_cost, final_distance = calculate_cost(route[-1], start_city)
    total_cost += final_cost
    total_distance += final_distance
    route.append(start_city)

    return route, total_cost, total_distance

best_route, best_cost, best_distance = nearest_neighbor(capitals_data)

print("Melhor rota encontrada:")
for city in best_route:
    print(city[0], end=" -> ")

print(f"\nCusto total: {round(best_cost, 2)}")
print(f"Distância total: {round(best_distance, 2)}")

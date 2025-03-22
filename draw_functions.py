import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pygame
from matplotlib.backends.backend_agg import FigureCanvasAgg
from typing import List, Tuple
from benchmark_attbrazil_capitals import *
import math

matplotlib.use("Agg")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

def draw_plot_fitness(screen, fitness_history):
     fig, ax = plt.subplots(figsize=(7, 2), dpi=100)
     cities = list(fitness_history.keys())
     fitness_values = list(fitness_history.values())
     
     ax.bar(cities, fitness_values, color='green')
     ax.set_title('Best Fitness per City')
     
     canvas = FigureCanvasAgg(fig)
     canvas.draw()
     raw_data = canvas.buffer_rgba()
     size = canvas.get_width_height()
     
     graph_surface = pygame.image.frombuffer(raw_data, size, "RGBA")
     screen.blit(graph_surface, (-30, 390))
     plt.close(fig)

def draw_plot(screen: pygame.Surface, x: list, y: list, x_label: str = 'Geração', y_label: str = 'Fitness') -> None:
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.plot(x, y, color="green", marker="o", linestyle="-", markersize=2)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True)

    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_argb()
    size = canvas.get_width_height()

    argb_array = np.frombuffer(raw_data, dtype=np.uint8).reshape((size[1], size[0], 4))
    rgb_array = np.delete(argb_array, 0, axis=2)
    raw_data = canvas.buffer_rgba()
    size = canvas.get_width_height()   

    surf = pygame.image.frombuffer(raw_data, size, "RGBA")
    screen.blit(surf, (10, -25))

    plt.close(fig)


def draw_cities(screen: pygame.Surface, cities_locations: List[Tuple[int, int]], rgb_color: Tuple[int, int, int], node_radius: int) -> None:
    for index, city_location in enumerate(cities_locations):
       
        pygame.draw.circle(screen, rgb_color, (city_location[0], city_location[1]), node_radius)
        draw_text(screen, capitals_states[index][0], (0, 0, 0), (city_location[0] + 12, city_location[1] - 12))


def draw_paths_with_arrow(screen: pygame.Surface, path: List[Tuple[float, float, float, float]], rgb_color: Tuple[int, int, int], width: int):
    if len(path) > 1:
        lat_lon_path = [(city[0], city[1]) for city in path]

        for i, city in enumerate(path):
            if i == 0:
                color = GREEN
            elif i == len(path) - 1:
                color = RED
            else:
                color = YELLOW

            pygame.draw.circle(screen, color, (city[0], city[1]), 5)
           
            if i < len(path) - 1:
                draw_arrow(screen,  lat_lon_path[i], lat_lon_path[i + 1], rgb_color)
        
        draw_arrow(screen, lat_lon_path[-1], lat_lon_path[0], rgb_color)
        return lat_lon_path

def draw_paths_seq(screen: pygame.Surface, path: List[Tuple[int, int]], rgb_color: Tuple[int, int, int]):
    if len(path) > 2:
        for index in range(len(path) - 1):
            mid_x = (path[index][0] + path[index + 1][0]) // 2
            mid_y = (path[index][1] + path[index + 1][1]) // 2
            draw_text(screen, str(index + 1), (0, 0, 0), (mid_x, mid_y))


def draw_text(screen: pygame.Surface, text: str, color: Tuple[int, int, int], city_location: Tuple[int, int]) -> None:
    font_size = 14
    font = pygame.font.SysFont("Arial", font_size)
    text_surface = font.render(text, True, color)

    text_position = text_surface.get_rect(midtop=(city_location[0], city_location[1] - 10))
    
    screen.blit(text_surface, text_position)


def draw_arrow(screen: pygame.Surface, start: Tuple[int, int], end: Tuple[int, int], color: Tuple[int, int, int], arrow_size: int = 6, width: int = 1):
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    stop_before = 10
    
    adjusted_end = (
        end[0] - stop_before * math.cos(angle),
        end[1] - stop_before * math.sin(angle)
    )

    left_arrow = (
        adjusted_end[0] - arrow_size * math.cos(angle - math.pi / 6),
        adjusted_end[1] - arrow_size * math.sin(angle - math.pi / 6),
    )
    right_arrow = (
        adjusted_end[0] - arrow_size * math.cos(angle + math.pi / 6),
        adjusted_end[1] - arrow_size * math.sin(angle + math.pi / 6),
    )

    pygame.draw.line(screen, color, start, adjusted_end, width)
    pygame.draw.polygon(screen, color, [adjusted_end, left_arrow, right_arrow])

def draw_paths(screen: pygame.Surface, path: List[Tuple[float, float, float, float]], rgb_color: Tuple[int, int, int], width: int):
    if len(path) > 1:
        lat_lon_path = [(city[0], city[1]) for city in path]

        for i, city in enumerate(path):
            if i == 0:
                color = GREEN
            elif i == len(path) - 1:
                color = RED
            else:
                color = YELLOW

            pygame.draw.circle(screen, color, (city[0], city[1]), 5)
            
        pygame.draw.lines(screen, rgb_color, True, lat_lon_path, width=width)  # Caminho fechado somente se houver mais de 2 pontos

        return lat_lon_path 
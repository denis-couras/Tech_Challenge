# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 13:33:42 2023

@author: mduques
"""

## problem source: https://people.sc.fsu.edu/~jburkardt/datasets/tsp/tsp.html
capitals_data = [
    # ("Sigla", (Latitude, Longitude), ICMS, Periculosidade, Pedágio, Velocidade Média, Qualidade da Estrada)
    ("AC", (-9.97499, -67.8243), 15, 6, 3, 70, 0.5),  # Rio Branco
    ("AL", (-9.66599, -35.735), 16, 5, 6, 80, 0.3),  # Maceió
    ("AP", (0.03493, -51.0664), 14, 4, 2, 75, 0.4), # Macapá
    ("AM", (-3.11903, -60.0217), 13, 9, 2, 60, 0.7),  # Manaus
    ("BA", (-12.9714, -38.5012), 19, 7, 8, 75, 0.4),  # Salvador
    ("CE", (-3.71722, -38.5433), 16, 5, 6, 95, 0.2),  # Fortaleza
    ("DF", (-15.8267, -47.9218), 15, 4, 5, 100, 0.1),  # Brasília
    ("ES", (-20.3155, -40.3128), 17, 5, 7, 90, 0.2),  # Vitória
    ("GO", (-16.6809, -49.2533), 14, 4, 4, 90, 0.1),  # Goiânia
    ("MA", (-2.52972, -44.3028), 16, 7, 3, 75, 0.5),  # São Luís
    ("MT", (-15.6014, -56.0979), 14, 6, 5, 80, 0.3),  # Cuiabá
    ("MS", (-20.4697, -54.6201), 12, 4, 6, 95, 0.2),  # Campo Grande
    ("MG", (-19.9167, -43.9345), 17, 6, 12, 85, 0.2),  # Belo Horizonte
    ("PA", (-1.45502, -48.5024), 17, 8, 3, 70, 0.6),  # Belém
    ("PB", (-7.1216, -34.8829), 16, 5, 5, 85, 0.3),  # João Pessoa
    ("PR", (-25.4284, -49.2733), 14, 3, 7, 100, 0.1),  # Curitiba
    ("PE", (-8.04756, -34.877), 18, 6, 10, 80, 0.3),  # Recife
    ("PI", (-5.092, -42.8034), 15, 5, 4, 85, 0.4),  # Teresina
    ("RJ", (-22.9068, -43.1729), 20, 8, 10, 80, 0.5),  # Rio de Janeiro
    ("RN", (-5.79448, -35.211), 14, 5, 5, 85, 0.2),  # Natal
    ("RS", (-30.0346, -51.2177), 15, 5, 9, 85, 0.2),  # Porto Alegre
    ("RO", (-8.76194, -63.9039), 13, 7, 3, 70, 0.6),  # Porto Velho
    ("RR", (2.82384, -60.6758), 11, 4, 2, 75, 0.3), # Boa Vista
    ("SC", (-27.5949, -48.5482), 13, 3, 5, 100, 0.1),  # Florianópolis
    ("SP", (-23.5505, -46.6333), 18, 7, 15, 90, 0.3),  # São Paulo
    ("SE", (-10.9472, -37.0731), 15, 5, 6, 80, 0.4),  # Aracaju
    ("TO", (-10.184, -48.3336), 14, 5, 3, 85, 0.2),   # Palmas
]

capitals_states_old = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

capitals_states = [
    ("AC", 15, 6, 3, 70, 0.5),  # Acre
    ("AL", 16, 5, 6, 80, 0.3),  # Alagoas
    ("AP", 14, 4, 2, 75, 0.4),  # Amapá
    ("AM", 13, 9, 2, 60, 0.7),  # Amazonas
    ("BA", 19, 7, 8, 75, 0.4),  # Bahia
    ("CE", 16, 5, 6, 95, 0.2),  # Ceará
    ("DF", 15, 4, 5, 100, 0.1),  # Distrito Federal
    ("ES", 17, 5, 7, 90, 0.2),  # Espírito Santo
    ("GO", 14, 4, 4, 90, 0.1),  # Goiás
    ("MA", 16, 7, 3, 75, 0.5),  # Maranhão
    ("MT", 14, 6, 5, 80, 0.3),  # Mato Grosso
    ("MS", 12, 4, 6, 95, 0.2),  # Mato Grosso do Sul
    ("MG", 17, 6, 12, 85, 0.2),  # Minas Gerais
    ("PA", 17, 8, 3, 70, 0.6),  # Pará
    ("PB", 16, 5, 5, 85, 0.3),  # Paraíba
    ("PR", 14, 3, 7, 100, 0.1),  # Paraná
    ("PE", 18, 6, 10, 80, 0.3),  # Pernambuco
    ("PI", 15, 5, 4, 85, 0.4),  # Piauí
    ("RJ", 20, 8, 10, 80, 0.5),  # Rio de Janeiro
    ("RN", 14, 5, 5, 85, 0.2),  # Rio Grande do Norte
    ("RS", 15, 5, 9, 85, 0.2),  # Rio Grande do Sul
    ("RO", 13, 7, 3, 70, 0.6),  # Rondônia
    ("RR", 11, 4, 2, 75, 0.3),  # Roraima
    ("SC", 13, 3, 5, 100, 0.1),  # Santa Catarina
    ("SP", 18, 7, 15, 90, 0.3),  # São Paulo
    ("SE", 15, 5, 6, 80, 0.4),  # Sergipe
    ("TO", 14, 5, 3, 85, 0.2)   # Tocantins
]


capitals_locations = [
    (-9.97499, -67.8243),   # Rio Branco - AC
    (-9.66599, -35.735),    # Maceió - AL
    (0.03493, -51.0694),    # Macapá - AP
    (-3.11866, -60.0212),   # Manaus - AM
    (-12.9714, -38.5014),   # Salvador - BA
    (-3.71722, -38.5433),   # Fortaleza - CE
    (-15.7797, -47.9297),   # Brasília - DF
    (-20.3155, -40.3128),   # Vitória - ES
    (-16.6786, -49.2539),   # Goiânia - GO
    (-2.53073, -44.3068),   # São Luís - MA
    (-15.5989, -56.0949),   # Cuiabá - MT
    (-20.4428, -54.6464),   # Campo Grande - MS
    (-19.9167, -43.9345),   # Belo Horizonte - MG
    (-1.45502, -48.5024),   # Belém - PA
    (-7.1216, -34.8828),    # João Pessoa - PB
    (-25.4195, -49.2646),   # Curitiba - PR
    (-8.0476, -34.877),     # Recife - PE
    (-5.08921, -42.8016),   # Teresina - PI
    (-22.9068, -43.1729),   # Rio de Janeiro - RJ
    (-5.79448, -35.211),    # Natal - RN
    (-30.0346, -51.2177),   # Porto Alegre - RS
    (-8.76194, -63.9039),   # Porto Velho - RO
    (2.82384, -60.6753),    # Boa Vista - RR
    (-27.5954, -48.548),    # Florianópolis - SC
    (-23.5505, -46.6333),   # São Paulo - SP
    (-10.9472, -37.0731),   # Aracaju - SE
    (-10.184, -48.3336)     # Palmas - TO
]


capitals_order = [
    1, 14, 9, 22, 5, 18, 11, 7, 25, 6, 
    21, 16, 4, 2, 10, 17, 24, 13, 20, 8, 
    27, 15, 19, 23, 12, 26, 3, 1
]
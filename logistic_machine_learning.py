import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
from benchmark_attbrazil_capitals import capitals_data

# Configuração do problema
N_CITIES = 15
cities = np.array([point[1] for point in capitals_data[:N_CITIES]])

def calculate_distance(route):
    return sum(np.linalg.norm(route[i] - route[i+1]) for i in range(len(route) - 1)) + np.linalg.norm(route[-1] - route[0])

# Definição da rede neural para o Deep Q-Learning
class DQN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Inicialização do modelo, otimizador e memória de replay
input_size = 2 * N_CITIES
hidden_size = 128
output_size = N_CITIES

model = DQN(input_size, hidden_size, output_size)
optimizer = optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.MSELoss()

epsilon = 1.0  # Taxa de exploração
epsilon_decay = 0.995
min_epsilon = 0.01
gamma = 0.9  # Fator de desconto
memory = deque(maxlen=1000)

# Treinamento com Deep Q-Learning
for episode in range(500):
    state = cities.flatten()
    total_reward = 0
    route = []
    visited = set()
    
    while len(route) < N_CITIES:
        if random.random() < epsilon:
            action = random.choice([i for i in range(N_CITIES) if i not in visited])
        else:
            state_tensor = torch.tensor(state, dtype=torch.float32)
            q_values = model(state_tensor)
            action = torch.argmax(q_values).item()
        
        if action in visited:
            continue
        
        visited.add(action)
        route.append(cities[action])
        if len(route) > 1:
            reward = -np.linalg.norm(route[-1] - route[-2])
        else:
            reward = 0
        
        next_state = np.zeros((N_CITIES, 2))
        next_state[:len(route)] = route  # Copia as cidades já visitadas
        next_state = next_state.flatten()
        memory.append((state, action, reward, next_state))
        state = next_state
        total_reward += reward
    
    # Atualização do modelo
    if len(memory) > 32:
        batch = random.sample(memory, 32)
        for state, action, reward, next_state in batch:
            state_tensor = torch.tensor(state, dtype=torch.float32)
            next_state_tensor = torch.tensor(next_state, dtype=torch.float32)
            q_values = model(state_tensor)
            next_q_values = model(next_state_tensor).detach()
            target = reward + gamma * torch.max(next_q_values)
            loss = loss_fn(q_values[action], target)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    
    epsilon = max(min_epsilon, epsilon * epsilon_decay)
    if episode % 50 == 0:
        print(f"Episode {episode}: Total Reward = {total_reward}")

# Comparação com abordagem tradicional
best_nn_solution = route
best_nn_distance = calculate_distance(best_nn_solution)
print(f"Melhor solução ML (DQN): {best_nn_distance}")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Константы
G = 6.67430e-11  # Гравитационная постоянная, м^3 кг^-1 с^-2
AU = 1.496e11  # Астрономическая единица, метры
DAY = 86400  # Секунды в дне

# Параметры планет (масса в кг, радиус орбиты в метрах, начальная скорость в м/с)
planets = {
    'Mercury': {'mass': 3.30e23, 'distance': 0.39 * AU, 'velocity': 47.87e3},
    'Venus': {'mass': 4.87e24, 'distance': 0.72 * AU, 'velocity': 35.02e3},
    'Earth': {'mass': 5.97e24, 'distance': 1.00 * AU, 'velocity': 29.78e3},
    'Mars': {'mass': 0.642e24, 'distance': 1.52 * AU, 'velocity': 24.07e3},
    'Jupiter': {'mass': 1898e24, 'distance': 5.20 * AU, 'velocity': 13.07e3},
    'Saturn': {'mass': 568e24, 'distance': 9.58 * AU, 'velocity': 9.69e3},
    'Uranus': {'mass': 86.8e24, 'distance': 19.22 * AU, 'velocity': 6.81e3},
    'Neptune': {'mass': 102e24, 'distance': 30.05 * AU, 'velocity': 5.43e3},
}

# Начальные позиции и скорости планет
positions = []
velocities = []
for planet in planets.values():
    positions.append(np.array([planet['distance'], 0.0]))
    velocities.append(np.array([0.0, planet['velocity']]))
positions = np.array(positions)
velocities = np.array(velocities)

# Позиция Солнца
sun_position = np.array([0.0, 0.0])

# Масса Солнца
sun_mass = 1.989e30

# Время шага симуляции (1 день)
dt = DAY

def compute_accelerations(positions, sun_position, sun_mass, planet_masses):
    accelerations = np.zeros_like(positions)
    for i, position in enumerate(positions):
        direction_to_sun = sun_position - position
        distance_to_sun = np.linalg.norm(direction_to_sun)
        accelerations[i] = G * sun_mass * direction_to_sun / distance_to_sun**3

        for j, other_position in enumerate(positions):
            if i != j:
                direction_to_other = other_position - position
                distance_to_other = np.linalg.norm(direction_to_other)
                accelerations[i] += G * planet_masses[j] * direction_to_other / distance_to_other**3

    return accelerations

# Анимация
fig, ax = plt.subplots()
lines = []
for i in range(len(planets)):
    line, = ax.plot([], [], 'o', label=list(planets.keys())[i])
    lines.append(line)
ax.plot(0, 0, 'o', color='yellow', label='Sun')
ax.legend()
ax.set_xlim(-35 * AU, 35 * AU)
ax.set_ylim(-35 * AU, 35 * AU)

def init():
    for line in lines:
        line.set_data([], [])
    return lines

def update(frame):
    global positions, velocities
    accelerations = compute_accelerations(positions, sun_position, sun_mass, [planet['mass'] for planet in planets.values()])
    velocities += accelerations * dt
    positions += velocities * dt
    for i, line in enumerate(lines):
        line.set_data([positions[i, 0]], [positions[i, 1]])
    return lines

ani = animation.FuncAnimation(fig, update, frames=365, init_func=init, blit=True, interval=20)
plt.show()

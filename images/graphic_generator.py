import matplotlib.pyplot as plt
import math

# Ustawienia figury: czarne tło, rozmiar 4x4 cala
fig, ax = plt.subplots(figsize=(4, 4), facecolor='black')

# Liczba wierzchołków (sześciokąt)
n = 6

# Obliczamy położenie wierzchołków na jednostkowym okręgu, zaczynając od 90°
vertices = []
for i in range(n):
    angle = math.radians(90 - i * (360 / n))
    x = math.cos(angle)
    y = math.sin(angle)
    vertices.append((x, y))

# Rysujemy linie łączące każdy wierzchołek z każdym (pełny graf)
line_width = 3  # Grubość linii
for i in range(n):
    for j in range(i + 1, n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[j]
        ax.plot([x1, x2], [y1, y2], color='white', linewidth=line_width)

# Dodajemy kółka w miejscach wierzchołków
node_radius = 0.08  # Promień kółek
for (x, y) in vertices:
    circle = plt.Circle((x, y), node_radius, color='white', fill=True)
    ax.add_patch(circle)

# Dodajemy napis "ADHD MANAGER" poniżej symbolu
ax.text(0, -1.3, 'ADHD MANAGER', color='white',
        fontsize=20, ha='center', va='center', fontweight='bold')

# Ukrywamy osie i zachowujemy proporcje
ax.set_aspect('equal', 'box')
ax.axis('off')

# Zapisujemy grafikę do pliku
plt.savefig('adhd_manager_logo_more_lines_full.png', dpi=300, bbox_inches='tight')
plt.show()

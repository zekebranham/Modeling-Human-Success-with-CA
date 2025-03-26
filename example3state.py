import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Convert rule number (0–2186) into 7-digit base-3 list
def rule_number_to_totalistic_rule(rule_number):
    digits = [0] * 7
    for i in range(6, -1, -1):
        digits[i] = rule_number % 3
        rule_number //= 3
    return digits

# Create rule map: total sum (0-6) -> new state (direct mapping)
def generate_totalistic_direct_rule(rule_number):
    rule_digits = rule_number_to_totalistic_rule(rule_number)
    return {s: rule_digits[s] for s in range(7)}

# Evolve the CA using direct mapping (instead of incrementing)
def evolve_totalistic_ca(initial_state, rule_map, steps):
    width = len(initial_state)
    ca = np.zeros((steps, width), dtype=int)
    ca[0] = initial_state

    for t in range(1, steps):
        for i in range(1, width - 1):  # Exclude edges
            left = ca[t - 1, i - 1]
            center = ca[t - 1, i]
            right = ca[t - 1, i + 1]
            total = left + center + right
            ca[t, i] = rule_map[total]  # Direct mapping instead of mod 3

    return ca

# Plot with discrete 3-color colormap
def plot_totalistic_ca(ca, rule_number):
    colors = ['white', 'gray', 'black']
    cmap = mcolors.ListedColormap(colors)
    bounds = [-0.5, 0.5, 1.5, 2.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    plt.figure(figsize=(10, 6))
    plt.imshow(ca, cmap=cmap, norm=norm, interpolation='nearest', aspect='auto')
    plt.title(f"3-State Totalistic CA (Rule {rule_number})")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f"Totalistic3State_Rule{rule_number}_fixed.png", dpi=300)
    plt.show()

if __name__ == '__main__':
    width = 121  # Odd number for symmetry
    steps = 300
    rule_number = 1077  # Try others like 1062, 1749, etc.

    initial_state = np.zeros(width, dtype=int)
    initial_state[width // 2] = 1  # Single seed at center

    rule_map = generate_totalistic_direct_rule(rule_number)
    ca = evolve_totalistic_ca(initial_state, rule_map, steps)
    plot_totalistic_ca(ca, rule_number)

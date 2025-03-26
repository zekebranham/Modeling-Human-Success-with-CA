# Modified rule definitions with context-based logic
import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import itertools

# Define CA settings
NUM_GENERATIONS = 50
CA_WIDTH = 101
STATES = [0, 1, 2]

ALL_COMBINATIONS = list(itertools.product(STATES, repeat=3))

DEFAULT_RULES = {
    (2, 2, 2): 2,
    (0, 2, 0): 1,
    (1, 1, 1): 1,
    (0, 1, 0): 0,
    (1, 2, 0): 1,
    (0, 0, 2): 1,
    (2, 0, 1): 1,
}
for combo in ALL_COMBINATIONS:
    if combo not in DEFAULT_RULES:
        DEFAULT_RULES[combo] = combo[1]

"""
Rule Generation Summary:

Each rule in the 3-state Cellular Automaton is based on a 3-cell neighborhood (left, center, right),
which are interpreted as follows:
    - Left cell = Environment (e.g., peers, community, geographic region)
    - Center cell = Family structure or status
    - Right cell = Personal drive, ambition, or internal motivation

For each possible neighborhood combination (3^3 = 27), a resulting state is assigned
based on weighted probabilistic behavior determined by a behavioral model:

    - Balanced Model: ~30% Struggling, ~50% Stable, ~20% Thriving
    - Pessimistic Model: ~45% Struggling, ~45% Stable, ~10% Thriving
    - Optimistic Model: ~15% Struggling, ~50% Stable, ~35% Thriving

These rules are randomly generated at program start using the `generate_rule_set()` function,
and produce deterministic behavior across the full rule set, while still maintaining
the flavor of the social lens (optimistic/pessimistic/balanced).

This approach allows you to model socioeconomic mobility from different ideological worldviews
and investigate how structural patterns emerge from simple, interpretable local rules.
"""

class CAApp:
    def __init__(self, master):
        self.master = master
        master.title("3-State CA: Deterministic Phase")

        self.cells = [tk.IntVar(value=0) for _ in range(CA_WIDTH)]
        self.spinboxes = []

        self.rules = DEFAULT_RULES.copy()
        self.randomness_enabled = tk.BooleanVar(value=True) #NEW ADDED RANDOMNESS
        self.randomness_level = tk.DoubleVar(value=0.10)  # Higher default randomness for stochastic phase

        tk.Label(master, text="Initial Generation (0=Struggling, 1=Stable, 2=Thriving):").pack(pady=(5, 0))
        self.init_frame = tk.Frame(master)
        self.init_frame.pack()
        upper_row = tk.Frame(self.init_frame)
        lower_row = tk.Frame(self.init_frame)
        upper_row.pack()
        lower_row.pack()
        for i in range(CA_WIDTH):
            sb = tk.Spinbox(upper_row if i < CA_WIDTH // 2 else lower_row, from_=0, to=2, width=2, textvariable=self.cells[i])
            sb.pack(side='left')
            self.spinboxes.append(sb)

        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Initialize Single Thriving Center", command=self.init_single_center).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Randomize Initial Generation", command=self.randomize_initial).pack(side='left', padx=5)


        self.randomness_enabled = tk.BooleanVar(value=True)
        self.randomness_level = tk.DoubleVar(value=0.01)
        tk.Checkbutton(master, text="Enable Random Events", variable=self.randomness_enabled).pack()
        tk.Label(master, text="Randomness Level (0.0 - 1.0):").pack()
        tk.Scale(master, from_=0.0, to=0.2, resolution=0.01, orient=tk.HORIZONTAL, variable=self.randomness_level).pack()

        tk.Button(master, text="Run Simulation", command=self.run_simulation).pack(pady=10)
        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack()

    def init_single_center(self):
        for i, var in enumerate(self.cells):
            var.set(0)
        self.cells[CA_WIDTH // 2].set(2)

    def randomize_initial(self):
        for var in self.cells:
            var.set(random.choice(STATES))

    def next_state(self, left, center, right):
        if self.randomness_enabled.get() and random.random() < self.randomness_level.get():
            return random.choice(STATES)
        return self.rules.get((left, center, right), center)

    def evolve(self, initial_row):
        generations = [initial_row]
        current = initial_row.copy()
        for _ in range(NUM_GENERATIONS - 1):
            next_gen = []
            for i in range(len(current)):
                l = current[i - 1] if i > 0 else 0
                c = current[i]
                r = current[i + 1] if i < len(current) - 1 else 0
                next_gen.append(self.next_state(l, c, r))
            generations.append(next_gen)
            current = next_gen
        return generations

    def display_ca(self, generations):
        arr = np.array(generations)
        cmap = ListedColormap(['blue', 'gold', 'green'])  # State 0,1,2

        fig, axs = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [4, 1]})

        im = axs[0].imshow(arr, cmap=cmap, interpolation='nearest')
        axs[0].set_title("3-State CA: Stochastic Phase")
        axs[0].axis('off')

        # Move the legend outside the plot (top-right corner)
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='blue', label='Struggling (0)'),
            Patch(facecolor='gold', label='Stable (1)'),
            Patch(facecolor='green', label='Thriving (2)')
        ]
        axs[0].legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.0, 0.5), frameon=False)

        # Line chart of state distribution
        state_0 = [row.count(0) for row in generations]
        state_1 = [row.count(1) for row in generations]
        state_2 = [row.count(2) for row in generations]

        axs[1].plot(state_0, color='blue')
        axs[1].plot(state_1, color='gold')
        axs[1].plot(state_2, color='green')
        axs[1].set_title("State Distribution Over Time")
        axs[1].set_xlabel("Generation")
        axs[1].set_ylabel("Count")
        axs[1].legend(loc='upper right')

        fig.tight_layout()
        return fig


    def run_simulation(self):
        init = [var.get() for var in self.cells]
        generations = self.evolve(init)
        fig = self.display_ca(generations)

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = CAApp(root)
    root.mainloop()
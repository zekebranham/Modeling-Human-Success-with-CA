import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import itertools
import csv

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

class CAApp:
    def __init__(self, master):
        self.master = master
        master.title("3-State CA: Human Success Simulator")

        self.cells = [tk.IntVar(value=0) for _ in range(CA_WIDTH)]
        self.spinboxes = []

        self.rules = DEFAULT_RULES.copy()
        self.randomness_enabled = tk.BooleanVar(value=True)
        self.randomness_level = tk.DoubleVar(value=0.01)

        tk.Label(master, text="Initial Generation (0=Struggling, 1=Stable, 2=Thriving):").pack()
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

        tk.Checkbutton(master, text="Enable Random Events", variable=self.randomness_enabled).pack()
        tk.Label(master, text="Randomness Level (0.0 - 1.0):").pack()
        tk.Scale(master, from_=0.0, to=0.2, resolution=0.01, orient=tk.HORIZONTAL, variable=self.randomness_level).pack()

        tk.Button(master, text="Run Simulation", command=self.run_simulation).pack(pady=10)
        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack()
        self.export_btn = tk.Button(master, text="Export to CSV", command=self.export_csv)
        self.export_btn.pack(pady=5)

        self.generations = []
        self.transition_counts = []

    def init_single_center(self):
        for i, var in enumerate(self.cells):
            var.set(0)
        center_index = CA_WIDTH // 2
        self.cells[center_index].set(2)

    def randomize_initial(self):
        for var in self.cells:
            var.set(random.choice(STATES))

    def next_state(self, left, center, right): #most of the changes are here from Phase IV
        if self.randomness_enabled.get() and random.random() < self.randomness_level.get(): #randomness (Phase IV)
            return random.choice(STATES), 'random'

        thriving_neighbors = [left, right].count(2) # Inheritance: 2 neighbors are thriving. (Phase V)
        if center < 2 and thriving_neighbors == 2:
            return min(center + 1, 2), 'inheritance'

        if center > 0 and left == 0 and right == 0: # Intervention: Struggling neighborhood pulls you down. (Phase V)
            return max(center - 1, 0), 'intervention'

        return self.rules.get((left, center, right), center), 'rule'

    def evolve(self, initial_row):
        generations = [initial_row]
        transitions = [] #for more chart analysis later
        current = initial_row.copy()
        for _ in range(NUM_GENERATIONS - 1):
            next_gen = []
            transition_count = {'random': 0, 'inheritance': 0, 'intervention': 0, 'rule': 0}
            for i in range(len(current)):
                l = current[i - 1] if i > 0 else 0
                c = current[i]
                r = current[i + 1] if i < len(current) - 1 else 0
                new_state, reason = self.next_state(l, c, r)
                transition_count[reason] += 1
                next_gen.append(new_state)
            generations.append(next_gen)
            transitions.append(transition_count)
            current = next_gen
        return generations, transitions

    def display_ca(self, generations, transitions):
        arr = np.array(generations)
        cmap = ListedColormap(['blue', 'gold', 'green'])  # State 0,1,2
        fig, axs = plt.subplots(3, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [4, 1, 1]})

        axs[0].imshow(arr, cmap=cmap, interpolation='nearest')
        axs[0].set_title("3-State Cellular Automaton: Human Success Simulation")
        axs[0].axis('off')

        # Move the legend outside the plot (top-right corner)
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='blue', label='Struggling (0)'),
            Patch(facecolor='gold', label='Stable (1)'),
            Patch(facecolor='green', label='Thriving (2)')
        ]
        axs[0].legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.0, 0.5), frameon=False)

        # Plot state distribution
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

        reasons = ['rule', 'inheritance', 'intervention', 'random']
        for reason in reasons:
            axs[2].plot([t[reason] for t in transitions])
        axs[2].legend() #Transitions Over Time Chart
        axs[2].set_xlabel("Generation")
        axs[2].set_ylabel("Count")

        fig.tight_layout()
        return fig

    def run_simulation(self):
        init = [var.get() for var in self.cells]
        self.generations, self.transition_counts = self.evolve(init)
        fig = self.display_ca(self.generations, self.transition_counts)

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def export_csv(self):
        if not self.generations:
            messagebox.showwarning("Warning", "Please run the simulation first.")
            return
        with open("ca_simulation_export.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([f"Cell {i}" for i in range(CA_WIDTH)])
            for row in self.generations:
                writer.writerow(row)
        messagebox.showinfo("Success", "Simulation data exported to ca_simulation_export.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = CAApp(root)
    root.mainloop()

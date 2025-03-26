import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

"""
First introduction of three distinct states: struggling, stable, and thriving.
A handful of core rules define interactions (no randomness yet).
Demonstrates how a single successful agent can influence neighbors over generations in a controlled, deterministic way.
"""
NUM_GENERATIONS = 50
CA_WIDTH = 101
STATES = [0, 1, 2] #0 = struggling, 1 = stable 2 = thriving

# Simplified early rules for basic 3-state logic
BASIC_RULES = {
    (2, 2, 2): 2,
    (0, 2, 0): 1,
    (1, 1, 1): 1,
    (0, 1, 0): 0,
}
#unlisted combinations defult to the center value

class CAApp:
    def __init__(self, master):
        self.master = master
        master.title("Phase 2: Basic 3-State CA")

        self.cells = [tk.IntVar(value=0) for _ in range(CA_WIDTH)]
        self.spinboxes = []

        self.rules = BASIC_RULES.copy()

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

        tk.Button(master, text="Run Simulation", command=self.run_simulation).pack(pady=10)

        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack()

    def init_single_center(self):
        for i, var in enumerate(self.cells):
            var.set(0)
        self.cells[CA_WIDTH // 2].set(2)

    def randomize_initial(self):
        import random
        for var in self.cells:
            var.set(random.choice(STATES))

    def next_state(self, left, center, right):
        return self.rules.get((left, center, right), center) #Checks if left, center, right triplet combo exists in self.rules, if not, centervalue default

    def evolve(self, initial_row): #this guy just generates new rows using the next_state() function above. Adds each new row to generations[]
        generations = [initial_row]
        current = initial_row.copy()
        for _ in range(NUM_GENERATIONS - 1):
            next_gen = []
            for i in range(len(current)):
                l = current[i - 1] if i > 0 else 0
                c = current[i]
                r = current[i + 1] if i < len(current) - 1 else 0 #whole bunch of stuff here, not all that important
                next_gen.append(self.next_state(l, c, r))
            generations.append(next_gen)
            current = next_gen
        return generations

    def display_ca(self, generations): #uses matplotlib to display the generations using the 3-color colormap using viridis
        arr = np.array(generations)
        cmap = ListedColormap(['blue', 'gold', 'green'])  # State 0,1,2

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(arr, cmap=cmap, interpolation='nearest')
        ax.set_title("Phase 2: 3-State Cellular Automaton")
        ax.axis('off')

         # Move the legend outside the plot (top-right corner)
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='blue', label='Struggling (0)'),
            Patch(facecolor='gold', label='Stable (1)'),
            Patch(facecolor='green', label='Thriving (2)')
        ]
        ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.0, 0.5), frameon=False)

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
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process

def generic_rule(rule_number):
    rule_bits = f"{rule_number:08b}"
    patterns = ["111", "110", "101", "100", "011", "010", "001", "000"]
    rule_map = {p: int(b) for p, b in zip(patterns, rule_bits)}

    def rule_fn(left, center, right):
        pattern = f"{left}{center}{right}"
        return rule_map[pattern]
    
    return rule_fn

def generate_automaton(rule_func, initial_state, steps):
    automaton = np.zeros((steps, len(initial_state)), dtype=int)
    automaton[0] = initial_state

    for i in range(1, steps):
        for j in range(1, len(initial_state) - 1):
            left, center, right = automaton[i - 1, j - 1], automaton[i - 1, j], automaton[i - 1, j + 1]
            automaton[i, j] = rule_func(left, center, right)

    return automaton

def run_and_save(rule_number, width=800, steps=300):
    initial_state = np.zeros(width, dtype=int)
    initial_state[width // 2] = 1
    rule_func = generic_rule(rule_number)
    automaton = generate_automaton(rule_func, initial_state, steps)

    plt.figure(figsize=(10, 10))
    plt.imshow(automaton, cmap='binary', interpolation='none', aspect='equal')
    plt.title(f"Rule {rule_number} Cellular Automaton", pad=20)
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    plt.savefig(f"Rule{rule_number}.png", dpi=400, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    import multiprocessing

    rules = [30, 90, 110, 126, 22, 4, 45, 54, 73, 135]
    processes = []

    for rule in rules:
        p = Process(target=run_and_save, args=(rule,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    
    print("All automaton images saved.")

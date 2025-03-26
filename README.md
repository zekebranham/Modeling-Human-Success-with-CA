# Human Success & Social Mobility with Cellular Automata

This repository contains a six-phase simulation project using 1D multi-state Cellular Automata (CA) to model generational human success, class mobility, and socio-economic structures. Each phase incrementally builds on the last, progressing from simple binary automata to complex social models incorporating randomness, inheritance, and societal worldviews.

---

## 🌐 Overview

The project simulates how local influences (e.g., environment, family, personal drive) affect long-term economic mobility across generations using Cellular Automata. The 3-state CA uses symbolic states:

- **0** = Struggling  
- **1** = Stable (Middle Class)  
- **2** = Thriving

Through six phases, this model demonstrates how simple rule-based systems can reflect and help visualize the emergence of social structures like the middle class, inheritance-based mobility, and structural inequality.

---

## 🔁 Phases Breakdown

| Phase | Description |
|-------|-------------|
| **Phase I** | `PhaseI_BinaryCA.py` — Basic 2-state CA using classic rules (e.g. Rule 30, Rule 110). Visual-only demo. |
| **Phase II** | `PhaseII_3_state.py` — Introduces 3 symbolic states with a deterministic rule set. GUI included. |
| **Phase III** | `PhaseIII_StochasticSuccess.py` — Adds randomness to simulate unpredictable life events and chance-driven mobility. |
| **Phase IV** | `PhaseIV_DeterministicRules.py` — Defines all 27 rules explicitly. Simulates structural systems like education, law, and zoning. |
| **Phase V** | `PhaseV_InheritanceIntervention.py` — Adds logic for inheritance (promotion) and systemic adversity (demotion). Tracks transition types. |
| **Phase VI** | `PhaseVI_BPO.py` — Implements behavioral worldviews: optimistic, balanced, pessimistic. Probabilistic rules reflect cultural or policy-based differences. |

---

## 🖥️ How to Run

Each phase includes a Python file with an interactive GUI (Tkinter-based).

### Requirements
- Python 3.x
- `matplotlib`
- `numpy`
- `tkinter` (standard with most Python installations)

### Example:
```bash
python PhaseIV_DeterministicRules.py

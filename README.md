# 🐔 SAT Solver for the River Crossing Minimization Problem

## 1. Project Overview

This project implements a solution to the **Constrained Chicken Problem**—a variation of the classic river crossing puzzle—by reducing it to the **Boolean Satisfiability Problem (SAT)**. The core objective is to find the minimum time ($T$) required for all chickens to cross a river under strict resource and speed constraints.

The solution uses Python's **PySAT** library with the **Minicard** solver, demonstrating the application of formal logic and complexity theory to solve a minimization problem.

***

## 2. Problem Constraints (The Rules)

The problem involves $N$ chickens with individual crossing times ($T_i$) and a boat with capacity $C$.

### Key Constraints:
* **Speed Rule:** The trip duration is determined by the maximum $T_i$ of all passengers.
* **Capacity:** The number of passengers ($C'$) must be less than or equal to the boat's capacity ($C$).
* **Single Resource:** Only one boat is available, requiring alternating journeys.
* **Rower:** At least one chicken must be in the boat for any journey.

## 3. Methodology: Reduction and Implementation

### A. The Reduction 
The problem is reduced to SAT by defining a set of boolean variables indexed by time ($t$) and chicken ($p$). The final formula ($\Phi$) is the conjunction of constraints ensuring validity, speed adherence, and resource exclusion. The reduction is guaranteed to be **polynomial in time** relative to the size of the input ($N$ and $T$).

### B. Implementation 
The solution is implemented in Python within the `project.py` file:

| Function | Role | Method |
| :--- | :--- | :--- |
| **`gen_solution`** | The Decision Problem | Encodes all constraints (Duration, Travel Lock, Capacity) into FNC clauses. Returns a valid set of moves if solvable in $T$, otherwise `None`. |
| **`find_duration`** | The Minimization Problem | Employs a linear search starting from the minimal physical requirement ($\max(T_i)$) and increments $T$ until `gen_solution` returns a solution. |

**Core Logic Highlights:**
* **Travel Lock:** Auxiliary variables are used to explicitly forbid any new departure while a trip is still in transit, enforcing the "single barque" rule.
* **Capacity:** Implemented efficiently using `solver.add_atmost` (native cardinality constraint handling).

***

## 4. How to Run

To run the full minimization solver, you must have the required SAT library installed.

1.  **Install PySAT:**
    ```bash
    pip install python-sat
    ```
2.  **Execute the Solver via the Tests (Find Minimal Time):**
    The main logic resides in `find_duration`. 
    ```bash
    python tests.py
    ```

**(Example of run)**
For the instance $T_i=[1, 3, 6, 8]$ and $C=2$, the minimal time found is $T=18$.
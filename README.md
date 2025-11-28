#  SAT Solver for the River Crossing Minimization Problem

## 1. Project Overview

[cite_start]This project implements a solution to the **Constrained Chicken Problem**—a variation of the classic river crossing puzzle—by reducing it to the **Boolean Satisfiability Problem (SAT)**[cite: 20, 24]. [cite_start]The core objective is to find the minimum time ($T$) required for all chickens to cross a river under strict resource and speed constraints[cite: 13, 23].

[cite_start]The solution uses Python's **PySAT** library with the **Minicard** solver [cite: 26, 29][cite_start], demonstrating the application of formal logic and complexity theory to solve a minimization problem[cite: 20, 21].

***

## 2. Problem Constraints (The Rules)

[cite_start]The problem involves $N$ chickens with individual crossing times ($T_i$) and a boat with capacity $C$[cite: 5, 13].

### Key Constraints:
* [cite_start]**Speed Rule:** The trip duration is determined by the maximum $T_i$ of all passengers[cite: 7, 10].
* [cite_start]**Capacity:** The number of passengers ($C'$) must be less than or equal to the boat's capacity ($C$)[cite: 5, 7].
* [cite_start]**Single Resource:** Only one boat is available, requiring alternating journeys[cite: 12].
* [cite_start]**Rower:** At least one chicken must be in the boat for any journey[cite: 12].

## 3. Methodology: Reduction and Implementation

### A. The Reduction (Q1)
The problem is reduced to SAT by defining a set of boolean variables indexed by time ($t$) and chicken ($p$). The final formula ($\Phi$) is the conjunction of constraints ensuring validity, speed adherence, and resource exclusion. [cite_start]The reduction is guaranteed to be **polynomial in time** relative to the size of the input ($N$ and $T$)[cite: 24].

### B. Implementation (Q2 & Q3)
The solution is implemented in Python within the `project.py` file:

| Function | Role | Method |
| :--- | :--- | :--- |
| **`gen_solution`** | The Decision Problem | Encodes all constraints (Duration, Travel Lock, Capacity) into FNC clauses. [cite_start]Returns a valid set of moves if solvable in $T$, otherwise `None`[cite: 32]. |
| **`find_duration`** | The Minimization Problem | [cite_start]Employs a linear search starting from the minimal physical requirement ($\max(T_i)$) and increments $T$ until `gen_solution` returns a solution[cite: 23, 31, 35]. |

**Core Logic Highlights:**
* **Travel Lock:** Auxiliary variables are used to explicitly forbid any new departure while a trip is still in transit, enforcing the "single barque" rule.
* [cite_start]**Capacity:** Implemented efficiently using `solver.add_atmost` (native cardinality constraint handling)[cite: 29, 82].

***

## 4. How to Run

To run the full minimization solver, you must have the required SAT library installed.

1.  **Install PySAT:**
    ```bash
    pip install python-sat
    ```
2.  **Execute the Solver (Find Minimal Time):**
    The main logic resides in `find_duration`. Assuming you have a test block in your file:
    ```bash
    python project.py
    ```

**(Example from the assignment)**
[cite_start]For the instance $T_i=[1, 3, 6, 8]$ and $C=2$, the minimal time found is $T=18$[cite: 15, 33].
```markdown
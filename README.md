# Thermometers MIP Solver

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Thermometers puzzle solver using mathematical programming.

## Overview

Thermometers is a logic puzzle where you must fill thermometers on a grid with mercury according to these rules:

- **Continuous filling from bulb** - thermometers fill from bulb end without gaps
- **Row and column constraints** - each row/column must have a specific number of filled cells

This solver models the puzzle as a **Mixed Integer Programming (MIP)** problem to find solutions.

## Installation

```bash
pip install thermometers-mip-solver
```

## Requirements

- Python 3.9+
- Google OR-Tools
- pytest (for testing)

## Usage

```python
from thermometers_mip_solver import ThermometerPuzzle, ThermometersSolver

# Define a 4x4 puzzle using waypoints to describe thermometer shapes
puzzle = ThermometerPuzzle(
    row_sums=[1, 3, 2, 1],              # Mercury cells per row
    col_sums=[1, 2, 2, 2],              # Mercury cells per column
    thermometer_waypoints=[
        [(0, 2), (0, 0)],               # Horizontal thermometer
        [(0, 3), (1, 3)],               # Vertical thermometer
        [(1, 0), (2, 0)],               # Vertical thermometer
        [(1, 1), (1, 2)],               # Horizontal thermometer
        [(2, 1), (2, 3)],               # Horizontal thermometer
        [(3, 1), (3, 0)],               # Horizontal thermometer
        [(3, 3), (3, 2)]                # Horizontal thermometer
    ]
)

# Solve the puzzle
solver = ThermometersSolver(puzzle)
solution = solver.solve()

if solution:
    print(f"Solution found! Filled positions: {solution}")
    
    # Validate the solution
    is_valid, errors = puzzle.validate_solution(solution)
    print(f"Solution is valid: {is_valid}")
    
    # Get solver information
    info = solver.get_solver_info()
    print(f"Model consists of {info['variables']} variables and {info['constraints']} constraints")
else:
    print("No solution exists")
```

## Example Puzzles

### Simple 4x4 Puzzle

![4x4 Puzzle](images/4x4_curved_19,253,725.png)
![4x4 Solution](images/4x4_curved_19,253,725_solution.png)

This curved 4x4 puzzle demonstrates thermometers with multiple waypoints, creating L-shaped and more complex paths.

### Complex 6x6 Puzzle

![6x6 Puzzle](images/6x6_14,708,221.png)
![6x6 Solution](images/6x6_14,708,221_solution.png)

This 6x6 puzzle shows how the solver handles larger grids with multiple thermometers of varying lengths and orientations.

## Testing

The project uses pytest for testing:

```bash
pytest                                          # Run all tests
pytest --cov=thermometers_mip_solver           # Run with coverage
```

## Mathematical Model

The solver uses **Mixed Integer Programming (MIP)** to model the puzzle constraints. Below is the complete mathematical formulation:

### Problem Definition

Given:
- An **m × n** grid representing the puzzle board
- **Row mercury requirements** R = {r₁, r₂, ..., rₘ} where rᵢ is the required number of mercury-filled cells in row i
- **Column mercury requirements** C = {c₁, c₂, ..., cₙ} where cⱼ is the required number of mercury-filled cells in column j
- **Thermometer paths** T = {T₁, T₂, ..., Tₖ} where each Tᵢ is an ordered sequence of cell positions representing a thermometer

**Objective:** Find which cells to fill with mercury to satisfy all Thermometers puzzle rules.

### Sets and Indices

| Symbol | Definition |
|--------|------------|
| **I** | Set of row indices: I = {0, 1, ..., m-1} |
| **J** | Set of column indices: J = {0, 1, ..., n-1} |
| **T** | Set of thermometers: T = {T₁, T₂, ..., Tₖ} |
| **Tᵢ** | Ordered sequence of positions for thermometer i: Tᵢ = [(r₁,c₁), (r₂,c₂), ..., (rₗᵢ,cₗᵢ)] |

### Decision Variables

| Variable | Domain | Definition |
|----------|--------|------------|
| **x_{i,j}** | {0, 1} | 1 if cell (i,j) is filled with mercury, 0 otherwise |

### Objective Function

This is a constraint satisfaction problem:

```
minimize 0
```

### Constraints

#### 1. Row Sum Constraints
Each row must contain exactly the required number of mercury-filled cells:

```
Σⱼ x_{i,j} = rᵢ    ∀i ∈ I
```

#### 2. Column Sum Constraints  
Each column must contain exactly the required number of mercury-filled cells:

```
Σᵢ x_{i,j} = cⱼ    ∀j ∈ J
```

#### 3. Thermometer Continuity Constraints
For each thermometer, mercury must fill continuously from the bulb (first position). If position k+1 in the thermometer is filled, then position k must also be filled:

```
x_{rₖ₊₁,cₖ₊₁} ≤ x_{rₖ,cₖ}    ∀Tᵢ ∈ T, ∀k ∈ {1, 2, ..., |Tᵢ|-1}
```

Where (rₖ,cₖ) and (rₖ₊₁,cₖ₊₁) are consecutive positions in thermometer Tᵢ.

### Complete MIP Formulation

**Variables:**
```
x_{i,j} ∈ {0,1}    ∀i ∈ I, ∀j ∈ J
```

**Objective:**
```
minimize 0
```

**Subject to:**
```
Σⱼ x_{i,j} = rᵢ                                    ∀i ∈ I         (Row sums)

Σᵢ x_{i,j} = cⱼ                                    ∀j ∈ J         (Column sums)

x_{rₖ₊₁,cₖ₊₁} ≤ x_{rₖ,cₖ}                          ∀Tᵢ ∈ T, ∀k    (Thermometer continuity)

x_{i,j} ∈ {0,1}                                    ∀i ∈ I, ∀j ∈ J (Binary variables)
```

### Key Features

- **Waypoint-based thermometer definition**: Thermometers are defined using waypoints that automatically expand to full paths
- **Continuous filling constraint**: Ensures mercury fills from bulb without gaps
- **Flexible shapes**: Supports straight, L-shaped, and complex curved thermometers
- **Efficient modeling**: Uses only essential constraints for fast solving

**Solver Backend**: Uses Google OR-Tools with SCIP optimizer by default.

## Algorithm Details

The solver workflow:

1. **Thermometer Path Expansion**: Waypoints are expanded into complete cell sequences using horizontal and vertical segments
2. **Variable Creation**: Binary variables created for each grid cell (filled/empty)
3. **Constraint Generation**: Three types of constraints ensure valid solutions:
   - Row/column sum constraints match target counts
   - Thermometer continuity constraints prevent gaps in mercury
4. **MIP Solving**: Google OR-Tools SCIP solver finds feasible solutions
5. **Solution Validation**: Results are verified against all puzzle rules

## License

This project is open source and available under the [MIT License](LICENSE).
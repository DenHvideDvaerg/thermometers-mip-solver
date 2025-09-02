# Thermometers MIP Solver

[![CI](https://github.com/DenHvideDvaerg/thermometers-mip-solver/actions/workflows/CI.yml/badge.svg)](https://github.com/DenHvideDvaerg/thermometers-mip-solver/actions/workflows/CI.yml)
[![Code Coverage](https://img.shields.io/codecov/c/github/DenHvideDvaerg/thermometers-mip-solver?color=blue)](https://codecov.io/gh/DenHvideDvaerg/thermometers-mip-solver)
[![PyPI version](https://img.shields.io/pypi/v/thermometers-mip-solver?color=green)](https://pypi.org/project/thermometers-mip-solver/)
[![Python](https://img.shields.io/pypi/pyversions/thermometers-mip-solver?color=blue)](https://pypi.org/project/thermometers-mip-solver/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Thermometers puzzle solver using mathematical programming.

## Overview

Thermometers is a logic puzzle where you must fill thermometers on a grid with mercury according to these rules:

- **Continuous filling from bulb** - thermometers fill from bulb end without gaps
- **Row and column constraints** - each row/column must have a specific number of filled cells
  - **Missing constraints variant** - supports puzzles where some row/column constraints are unknown (specified as `None`)

This solver models the puzzle as a **Mixed Integer Programming (MIP)** problem to find solutions.

## Installation

```bash
pip install thermometers-mip-solver
```

## Requirements

- Python 3.9+
- Google OR-Tools
- pytest (for testing)

## Example Puzzles

### 6x6 Puzzle with Straight Thermometers

This 6x6 puzzle demonstrates the solver with straight thermometers of various lengths and orientations:

| Puzzle | Solution |
|--------|----------|
| <img src="https://github.com/DenHvideDvaerg/thermometers-mip-solver/raw/main/images/6x6_14,708,221.png" width="400"> | <img src="https://github.com/DenHvideDvaerg/thermometers-mip-solver/raw/main/images/6x6_14,708,221_solution.png" width="400"> |

```python
def example_6x6():
    """6x6 Thermometers Puzzle ID: 14,708,221 from puzzle-thermometers.com"""
    puzzle = ThermometerPuzzle(
        row_sums=[3, 2, 1, 2, 5, 4],
        col_sums=[3, 2, 2, 4, 4, 2],
        thermometer_waypoints=[
            [(0, 0), (1, 0)],               # Vertical thermometer starting in row 0
            [(0, 2), (0, 1)],               # Horizontal thermometer starting in row 0
            [(1, 2), (1, 1)],               # Horizontal thermometer starting in row 1
            [(1, 3), (0, 3)],               # Vertical thermometer starting in row 1
            [(2, 0), (2, 2)],               # Horizontal thermometer starting in row 2
            [(3, 2), (3, 1)],               # Horizontal thermometer starting in row 3
            [(3, 3), (2, 3)],               # Vertical thermometer starting in row 3
            [(3, 4), (0, 4)],               # Long vertical thermometer starting in row 3
            [(3, 5), (0, 5)],               # Long vertical thermometer starting in row 3
            [(4, 0), (3, 0)],               # Vertical thermometer starting in row 4
            [(4, 1), (4, 3)],               # Horizontal thermometer starting in row 4
            [(4, 5), (4, 4)],               # Horizontal thermometer starting in row 4
            [(5, 0), (5, 5)],               # Long horizontal thermometer starting in row 5
        ]
    )
    return puzzle
```

### 5x5 Puzzle with Curved Thermometers and Missing Constraints

This 5x5 puzzle demonstrates advanced features: curved thermometers with multiple waypoints and missing row/column constraints (shown as `None`):

| Puzzle | Solution |
|--------|----------|
| <img src="https://github.com/DenHvideDvaerg/thermometers-mip-solver/raw/main/images/5x5_curved_missing_values.png" width="400"> | <img src="https://github.com/DenHvideDvaerg/thermometers-mip-solver/raw/main/images/5x5_curved_missing_values.png_solution.png" width="400"> |

```python
def example_5x5_curved_missing_values():
    """5x5 'Evil' Thermometers Puzzle from https://en.gridpuzzle.com/thermometers/evil-5"""
    puzzle = ThermometerPuzzle(
        row_sums=[2, 3, None, 5, None],         # Rows 2 and 4 have no constraint
        col_sums=[None, None, 1, 4, 4],         # Columns 0 and 1 have no constraint
        thermometer_waypoints=[
            [(0, 0), (0, 2), (2, 2)],            # L-shaped thermometer
            [(2, 0), (1, 0), (1, 1), (2, 1)],    # ∩-shaped thermometer
            [(2, 3), (0, 3), (0, 4)],            # L-shaped thermometer
            [(3, 0), (3, 3)],                    # Straight thermometer
            [(3, 4), (1, 4)],                    # Straight thermometer
            [(4, 0), (4, 1)],                    # Straight thermometer
            [(4, 2), (4, 4)],                    # Straight thermometer
        ]
    )
    return puzzle
```

## Usage

```python
from thermometers_mip_solver import ThermometerPuzzle, ThermometersSolver
import time

def solve_puzzle(puzzle, name):
    """Solve a thermometer puzzle and display results"""
    print(f"\n" + "="*60)
    print(f"SOLVING {name.upper()}")
    print("="*60)
    
    # Create and use the solver
    solver = ThermometersSolver(puzzle)
    
    print("Solver information:")
    info = solver.get_solver_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print("\nSolving...")
    start_time = time.time()
    solution = solver.solve(verbose=False)
    solve_time = time.time() - start_time
    
    if solution:
        print(f"\nSolution found in {solve_time:.3f} seconds!")
        print(f"Solution has {len(solution)} filled cells")
        print(f"Solution: {sorted(list(solution))}")
    else:
        print("No solution found by solver!")

# Load and solve example puzzles
puzzle_6x6 = example_6x6()
solve_puzzle(puzzle_6x6, "6x6")

puzzle_5x5_curved_missing = example_5x5_curved_missing_values()
solve_puzzle(puzzle_5x5_curved_missing, "5x5 Curved Missing Values")
```

### Output

```
============================================================
SOLVING 6X6
============================================================
Solver information:
  solver_type: SCIP 9.2.2 [LP solver: SoPlex 7.1.3]
  num_variables: 36
  num_constraints: 35
  grid_size: 6x6
  num_thermometers: 13
  total_cells: 36

Solving...

Solution found in 0.002 seconds!
Solution has 17 filled cells
Solution: [(0, 0), (0, 3), (0, 4), (1, 3), (1, 4), (2, 4), (3, 4), (3, 5), (4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (5, 0), (5, 1), (5, 2), (5, 3)]

============================================================
SOLVING 5X5 CURVED MISSING VALUES
============================================================
Solver information:
  solver_type: SCIP 9.2.2 [LP solver: SoPlex 7.1.3]
  num_variables: 25
  num_constraints: 24
  grid_size: 5x5
  num_thermometers: 7
  total_cells: 25

Solving...

Solution found in 0.002 seconds!
Solution has 14 filled cells
Solution: [(0, 3), (0, 4), (1, 0), (1, 3), (1, 4), (2, 0), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 0)]
```

## Waypoint System

The solver uses a **waypoint-based approach** to define thermometers. You only need to specify key turning points, and the system automatically expands them into complete thermometer paths:

- **Straight thermometers**: Define with start and end points: `[(0, 0), (0, 3)]`
- **Curved thermometers**: Add waypoints at each turn: `[(0, 0), (1, 0), (1, 1), (0, 1)]`
- **Path expansion**: Automatically fills in all cells between waypoints using horizontal/vertical segments
- **Validation**: Ensures all segments are properly aligned and thermometers have minimum 2 cells

## Testing

The project uses pytest for testing:

```bash
pytest                                          # Run all tests
pytest --cov=thermometers_mip_solver           # Run with coverage
```

## Mathematical Model

The solver uses **Mixed Integer Programming (MIP)** to model the puzzle constraints. Google OR-Tools provides the optimization framework, with SCIP as the default solver.

See the complete formulation in **[Complete Mathematical Model Documentation](https://github.com/DenHvideDvaerg/thermometers-mip-solver/blob/main/model.md)**

The model uses only three essential constraint types:
- **Row sum constraints** - ensure each row has the required number of filled cells
- **Column sum constraints** - ensure each column has the required number of filled cells  
- **Thermometer continuity constraints** - ensure mercury fills continuously from bulb without gaps

## License

This project is open source and available under the [MIT License](LICENSE.txt).

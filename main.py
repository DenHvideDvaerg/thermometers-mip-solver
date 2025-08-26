from thermometers_mip_solver.puzzle import ThermometerPuzzle
from thermometers_mip_solver.solver import ThermometersSolver
import time

def example_4x4():
    """4x4 Thermometers Puzzle ID: 9,377,208 from puzzle-thermometers.com"""
    puzzle = ThermometerPuzzle(
        row_sums=[1, 3, 2, 1],
        col_sums=[1, 2, 2, 2],
        thermometer_waypoints=[
            [(0, 2), (0, 0)],
            [(0, 3), (1, 3)],
            [(1, 0), (2, 0)],
            [(1, 1), (1, 2)],
            [(2, 1), (2, 3)],
            [(3, 1), (3, 0)],
            [(3, 3), (3, 2)]
        ]
    )
    return puzzle

def example_4x4_curved():
    """Curved 4x4 Thermometers Puzzle ID: 19,253,725 from puzzle-thermometers.com"""
    puzzle = ThermometerPuzzle(
        row_sums=[3, 1, 2, 1],
        col_sums=[1, 2, 3, 1],
        thermometer_waypoints=[
            [(0, 0), (1, 0), (1, 1), (0, 1)],    # U-shaped thermometer starting in row 0
            [(2, 2), (0, 2), (0, 3), (2, 3)],    # ∩-shaped thermometer starting in row 2
            [(3, 1), (2, 1), (2, 0), (3, 0)],    # ∩-shaped thermometer starting in row 3
            [(3, 3), (3, 2)],                    # Straight thermometer starting in row 3
        ]
    )
    return puzzle

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

def example_5x5_curved_missing_values():
    """5x5 'Evil' Thermometers Puzzle from https://en.gridpuzzle.com/thermometers/evil-5"""
    puzzle = ThermometerPuzzle(
        row_sums=[2, 3, None, 5, None],
        col_sums=[None, None, 1, 4, 4],
        thermometer_waypoints=[
            [(0, 0), (0, 2), (2, 2)],            # L-shaped thermometer starting in row 0
            [(2, 0), (1, 0), (1, 1), (2, 1)],    # ∩-shaped thermometer starting in row 2
            [(2, 3), (0, 3), (0, 4)],            # L-shaped thermometer starting in row 2
            [(3, 0), (3, 3)],                    # Straight thermometer starting in row 3
            [(3, 4), (1, 4)],                    # Straight thermometer starting in row 3
            [(4, 0), (4, 1)],                    # Straight thermometer starting in row 4
            [(4, 2), (4, 4)],                    # Straight thermometer starting in row 4
        ]
    )
    return puzzle

def main():
    puzzle_6x6 = example_6x6()
    solve_puzzle(puzzle_6x6, "6x6")

    puzzle_4x4_curved = example_4x4_curved()
    solve_puzzle(puzzle_4x4_curved, "4x4 Curved")

    puzzle_5x5_curved_missing_values = example_5x5_curved_missing_values()
    solve_puzzle(puzzle_5x5_curved_missing_values, "5x5 Curved Missing Values")


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

if __name__ == "__main__":
    main()
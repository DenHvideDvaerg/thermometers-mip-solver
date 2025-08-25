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
            [(0, 0), (1, 0), (1, 1), (0, 1)],
            [(2, 2), (0, 2), (0, 3), (2, 3)],
            [(3, 1), (2, 1), (2, 0), (3, 0)],
            [(3, 3), (3, 2)],
        ]
    )
    return puzzle

def example_6x6():
    """6x6 Thermometers Puzzle ID: 14,708,221 from puzzle-thermometers.com"""
    puzzle = ThermometerPuzzle(
        row_sums=[3, 2, 1, 2, 5, 4],
        col_sums=[3, 2, 2, 4, 4, 2],
        thermometer_waypoints=[
            # Thermometer 1: Vertical starting in (0,0)
            [(0, 0), (1, 0)],
            # Thermometer 2: Horizontal starting in (0,2)  
            [(0, 2), (0, 1)],
            # Thermometer 3: Horizontal starting in (1,2)
            [(1, 2), (1, 1)],
            # Thermometer 4: Vertical starting in (1, 3)
            [(1, 3), (0, 3)],
            # Thermometer 5: Horizontal starting in (2,0)
            [(2, 0), (2, 2)],
            # Thermometer 6: Horizontal starting in (3,2)
            [(3, 2), (3, 1)],
            # Thermometer 7: Vertical starting in (3,3)
            [(3, 3), (2, 3)],
            # Thermometer 8: Vertical starting in (3,4)
            [(3, 4), (0, 4)],
            # Thermometer 9: Vertical starting in (3,5)
            [(3, 5), (0, 5)],
            # Thermometer 10: Vertical starting in (4,0)
            [(4, 0), (3, 0)],
            # Thermometer 11: Horizontal starting in (4,1)
            [(4, 1), (4, 3)],
            # Thermometer 12: Horizontal starting in (4,5)
            [(4, 5), (4, 4)],
            # Thermometer 13: Vertical starting in (5,0)
            [(5, 0), (5, 5)],
        ]
    )
    return puzzle

def main():
    print("="*80)
    print("4x4 THERMOMETERS PUZZLE EXAMPLE")
    print("="*80)
    
    puzzle_4x4 = example_4x4()
    solve_puzzle(puzzle_4x4, "4x4")

    print("="*80)
    print("4x4 CURVED THERMOMETERS PUZZLE EXAMPLE")
    print("="*80)

    puzzle_4x4_curved = example_4x4_curved()
    solve_puzzle(puzzle_4x4_curved, "4x4 Curved")

    print("="*80)
    print("6x6 THERMOMETERS PUZZLE EXAMPLE")
    print("="*80)

    puzzle_6x6 = example_6x6()
    solve_puzzle(puzzle_6x6, "6x6")

def solve_puzzle(puzzle, name):
    """Solve a thermometer puzzle and display results"""
    print(f"\n{name} Puzzle: {puzzle}")
    
    # Show some thermometer examples
    print(f"\nFirst 3 thermometers in {name} puzzle:")
    for i, thermo in enumerate(puzzle.thermometers[:3]):
        print(f"  Thermometer {i+1}: {thermo}")
    
    print(f"\n" + "="*60)
    print(f"SOLVING {name.upper()} WITH MIP SOLVER")
    print("="*60)
    
    # Create and use the solver
    solver = ThermometersSolver(puzzle)
    
    print("Solver information:")
    info = solver.get_solver_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print("\nSolving...")
    start_time = time.time()
    solution = solver.solve(verbose=True)
    solve_time = time.time() - start_time
    
    if solution:
        print(f"\nSolution found in {solve_time:.3f} seconds!")
        print(f"Solution has {len(solution)} filled cells")
        
        # For 4x4, compare with manual solution
        if name == "4x4":
            manual_solution = {
                (0, 3), 
                (1,0),
                (1,1),
                (1,2),
                (2,1),
                (2,2),
                (3,3)
            }
            print(f"Manual solution: {sorted(manual_solution)}")
            print(f"MIP solution: {sorted(solution)}")
            print(f"Solutions match: {solution == manual_solution}")
        else:
            print(f"Solution: {sorted(list(solution))}")
    else:
        print("No solution found by solver!")

if __name__ == "__main__":
    main()
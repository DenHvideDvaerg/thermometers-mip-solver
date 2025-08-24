from thermometers_mip_solver.puzzle import ThermometerPuzzle
from thermometers_mip_solver.solver import ThermometersSolver

def main():
    # https://www.puzzle-thermometers.com/
    # 4x4 Thermometers Puzzle ID: 9,377,208
    puzzle = ThermometerPuzzle(
        row_sums=[1, 3, 2, 1],
        col_sums=[1, 2, 2, 2],
        thermometer_paths=[
            [(0, 2), (0, 1), (0,0)],  
            [(0,3), (1,3)],
            [(1, 0), (2, 0)],
            [(1, 1), (1, 2)],
            [(2, 1), (2, 2), (2, 3)],
            [(3, 1), (3, 0)],
            [(3, 3), (3, 2)]
        ]
    )

    print(f"Puzzle: {puzzle}")
    
    # Test manual solution validation
    manual_solution = {
        (0, 3), 
        (1,0),
        (1,1),
        (1,2),
        (2,1),
        (2,2),
        (3,3)
    }
    
    print(f"Manual solution is valid: {puzzle.is_valid_solution(manual_solution)}")
    
    # Show what each thermometer looks like
    print("\nThermometers:")
    for thermo in puzzle.thermometers:
        print(f"  {thermo}")
    
    print("\n" + "="*60)
    print("SOLVING WITH MIP SOLVER")
    print("="*60)
    
    # Create and use the solver
    solver = ThermometersSolver(puzzle)
    
    print("Solver information:")
    info = solver.get_solver_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print("\nSolving...")
    solution = solver.solve(verbose=True)
    
    if solution:
        print(f"\nMIP solution: {sorted(solution)}")
        print(f"Manual solution: {sorted(manual_solution)}")
        print(f"Solutions match: {solution == manual_solution}")
        
        print("\nChecking for multiple solutions...")
        all_solutions = solver.solve_iterative(max_num_solutions=3, verbose=True)
        print(f"\nTotal unique solutions found: {len(all_solutions)}")
        if len(all_solutions) > 1:
            print("Multiple solutions exist:")
            for i, sol in enumerate(all_solutions, 1):
                print(f"  Solution {i}: {sorted(sol)}")
        else:
            print("This puzzle has a unique solution!")
    else:
        print("No solution found by solver!")

if __name__ == "__main__":
    main()
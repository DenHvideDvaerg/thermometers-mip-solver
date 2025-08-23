from thermometers_mip_solver.puzzle import ThermometerPuzzle

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
    
    solution = {
        (0, 3), 
        (1,0),
        (1,1),
        (1,2),
        (2,1),
        (2,2),
        (3,3)
    }
    
    print(f"Valid solution: {puzzle.is_valid_solution(solution)}")
    
    # Show what each thermometer looks like
    for thermo in puzzle.thermometers:
        print(f"  {thermo}")

if __name__ == "__main__":
    main()
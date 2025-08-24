from .puzzle import ThermometerPuzzle
from ortools.linear_solver import pywraplp
from typing import Dict, Set, Tuple, Optional, List


class ThermometersSolver:
    """
    Mathematical programming solver for Thermometers puzzles.
    
    Uses Google OR-Tools to model the puzzle as an integer linear programming
    problem.
    """

    def __init__(self, puzzle: ThermometerPuzzle, solver_type: str = 'SCIP'):
        """
        Initialize the solver with a puzzle.
        
        Args:
            puzzle: The ThermometerPuzzle instance to solve
            solver_type: The OR-Tools solver to use (default: 'SCIP')
            
        Raises:
            ValueError: If puzzle is invalid or solver creation fails
        """
        
        if not isinstance(puzzle, ThermometerPuzzle):
            raise ValueError("Puzzle must be a ThermometerPuzzle instance")
        
        self.puzzle = puzzle
        self.solver = pywraplp.Solver.CreateSolver(solver_type)
        if not self.solver:
            raise ValueError(f"Could not create solver of type '{solver_type}'")
        
        # Dictionary to store binary variables for each cell
        self.cell_vars: Dict[Tuple[int, int], pywraplp.Variable] = {}
        
        # Define variable for each cell
        self._setup_variables()

        # Define constraints
        self._add_row_sum_constraints()
        self._add_col_sum_constraints()
        self._add_thermometer_constraints()

    def _setup_variables(self) -> None:
        """Create binary variables for each cell in the grid."""
        for row in range(self.puzzle.height):
            for col in range(self.puzzle.width):
                pos = (row, col)
                # Binary variable: 1 if cell is filled with mercury, 0 otherwise
                self.cell_vars[pos] = self.solver.BoolVar(f'cell_{row}_{col}')

    def _add_row_sum_constraints(self) -> None:
        """Add constraints ensuring each row has the correct number of filled cells."""
        for row in range(self.puzzle.height):
            row_vars = [self.cell_vars[(row, col)] for col in range(self.puzzle.width)]
            self.solver.Add(sum(row_vars) == self.puzzle.row_sums[row])

    def _add_col_sum_constraints(self) -> None:
        """Add constraints ensuring each column has the correct number of filled cells."""
        for col in range(self.puzzle.width):
            col_vars = [self.cell_vars[(row, col)] for row in range(self.puzzle.height)]
            self.solver.Add(sum(col_vars) == self.puzzle.col_sums[col])

    def _add_thermometer_constraints(self) -> None:
        """
        Add constraints ensuring thermometers are filled continuously from bulb.
        
        For each thermometer, if cell i+1 is filled, then cell i must also be filled.
        This ensures mercury fills continuously from the bulb (index 0) upward.
        """
        for thermo in self.puzzle.thermometers:
            positions = thermo.positions
            
            # For each pair of consecutive positions in the thermometer
            for i in range(len(positions) - 1):
                current_pos = positions[i]
                next_pos = positions[i + 1]
                
                current_var = self.cell_vars[current_pos]
                next_var = self.cell_vars[next_pos]
                
                # Constraint: next_var <= current_var
                # This means if next cell is filled (1), current must be filled (1)
                # If current is empty (0), next must be empty (0)
                self.solver.Add(next_var <= current_var)

    def solve(self, verbose: bool = False) -> Optional[Set[Tuple[int, int]]]:
        """
        Solve the puzzle and return the solution.
        
        Args:
            verbose: If True, print solver information
            
        Returns:
            Set of (row, col) positions that should be filled with mercury,
            or None if no solution exists
        """
        if verbose:
            print(f"Solving {self.puzzle.height}x{self.puzzle.width} puzzle with {len(self.puzzle.thermometers)} thermometers...")
        
        # Solve the problem
        status = self.solver.Solve()
        
        if verbose:
            print(f"Solver status: {self._status_to_string(status)}")
            if status == pywraplp.Solver.OPTIMAL:
                print(f"Objective value: {self.solver.Objective().Value()}")
                print(f"Time: {self.solver.WallTime()} ms")
        
        if status == pywraplp.Solver.OPTIMAL:
            # Extract solution
            solution = set()
            for pos, var in self.cell_vars.items():
                if var.solution_value() == 1:
                    solution.add(pos)
            
            if verbose:
                print(f"Solution found with {len(solution)} filled cells")
            
            return solution
        elif status == pywraplp.Solver.FEASIBLE:
             # This should not happen since the problem doesn't have an objective function
            raise RuntimeError("What the... Solver returned FEASIBLE status for a constraint satisfaction problem??")
        else:
            if verbose:
                print("No solution found")
            return None

    def solve_iterative(self, max_num_solutions: int = None, verbose: bool = False) -> List[Set[Tuple[int, int]]]:
        """
        Find multiple solutions to the puzzle.
        
        Uses solution cuts to iteratively find different solutions by excluding
        previously found solutions.
        
        Args:
            max_num_solutions: Maximum number of solutions to find (None for all)
            verbose: If True, print progress information
            
        Returns:
            List of solution sets, each containing (row, col) positions to fill
        """
        solutions = []
        iteration = 1
        
        if verbose:
            print(f"Finding multiple solutions (max: {max_num_solutions or 'unlimited'})...")
        
        while True:
            if verbose:
                print(f"Iteration {iteration}...")
            
            # Try to solve current problem
            solution = self.solve(verbose=False)
            
            if solution is None:
                if verbose:
                    print("No more solutions found")
                break
            
            # Check if we've seen this solution before (shouldn't happen with cuts)
            if solution in solutions:
                raise RuntimeError("Duplicate solution found (shouldn't happen)")
            
            solutions.append(solution)
            
            if verbose:
                print(f"Found solution {len(solutions)} with {len(solution)} filled cells")
            
            # Check if we've found enough solutions
            if max_num_solutions and len(solutions) >= max_num_solutions:
                if verbose:
                    print(f"Reached maximum number of solutions ({max_num_solutions})")
                break
            
            # Add cut to exclude this solution
            self._add_solution_cut(solution)
            iteration += 1
        
        if verbose:
            print(f"Total solutions found: {len(solutions)}")
        
        return solutions

    def _add_solution_cut(self, solution: Set[Tuple[int, int]]) -> None:
        """
        Add a constraint that excludes the given solution.
        
        Creates a constraint that forces at least one variable to have a different
        value than in the given solution.
        
        Args:
            solution: Set of positions that were filled in the solution to exclude
        """
        filled_vars = [self.cell_vars[pos] for pos in solution]        
        if filled_vars:
            self.solver.Add(sum(filled_vars) <= len(solution) - 1)

    def _status_to_string(self, status: int) -> str:
        """Convert solver status to readable string."""
        status_map = {
            pywraplp.Solver.OPTIMAL: "OPTIMAL",
            pywraplp.Solver.FEASIBLE: "FEASIBLE", 
            pywraplp.Solver.INFEASIBLE: "INFEASIBLE",
            pywraplp.Solver.UNBOUNDED: "UNBOUNDED",
            pywraplp.Solver.ABNORMAL: "ABNORMAL",
            pywraplp.Solver.NOT_SOLVED: "NOT_SOLVED"
        }
        return status_map.get(status, f"UNKNOWN({status})")

    def get_solver_info(self) -> Dict[str, any]:
        """Get information about the solver and problem size."""
        return {
            'solver_type': self.solver.SolverVersion(),
            'num_variables': self.solver.NumVariables(),
            'num_constraints': self.solver.NumConstraints(),
            'grid_size': f"{self.puzzle.height}x{self.puzzle.width}",
            'num_thermometers': len(self.puzzle.thermometers),
            'total_cells': self.puzzle.height * self.puzzle.width,
        }

    def validate_solution(self, solution: Set[Tuple[int, int]]) -> bool:
        """
        Validate that a solution satisfies all puzzle constraints.
        
        Args:
            solution: Set of positions to validate
            
        Returns:
            True if solution is valid, False otherwise
        """
        return self.puzzle.is_valid_solution(solution)
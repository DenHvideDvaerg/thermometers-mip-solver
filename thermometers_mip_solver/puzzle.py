from typing import List, Set, Tuple, Optional


class Thermometer:
    """
    Represents a thermometer as a sequence of connected cells.
    Mercury fills from the bulb (first position) towards the top.
    """
    
    def __init__(self, thermometer_id: int, positions: List[Tuple[int, int]]):
        """
        Args:
            thermometer_id: Unique identifier
            positions: List of (row, col) tuples from bulb to top
        """
        if not positions:
            raise ValueError("Thermometer must have at least one position")
        
        if len(set(positions)) != len(positions):
            raise ValueError("Thermometer cannot have duplicate positions")
        
        self.id = thermometer_id
        self.positions = positions.copy()
        self._validate_connectivity()
    
    def _validate_connectivity(self) -> None:
        """Ensure all positions are adjacent."""
        for i in range(len(self.positions) - 1):
            r1, c1 = self.positions[i]
            r2, c2 = self.positions[i + 1]
            # Adjacent means exactly 1 step in one direction
            if abs(r1 - r2) + abs(c1 - c2) != 1:
                raise ValueError(f"Positions ({r1},{c1}) and ({r2},{c2}) are not adjacent")
    
    def is_valid_fill_state(self, filled_positions: Set[Tuple[int, int]]) -> bool:
        """Check if filled positions form valid mercury fill from bulb."""
        # Find which of our positions are filled
        our_filled = [pos for pos in self.positions if pos in filled_positions]
        
        if not our_filled:
            return True  # Empty is valid
        
        # Must be a continuous sequence from the bulb (index 0)
        filled_indices = [self.positions.index(pos) for pos in our_filled]
        filled_indices.sort()
        
        return filled_indices == list(range(len(filled_indices)))
    
    @property
    def length(self) -> int:
        """Get the length of the thermometer."""
        return len(self.positions)
    
    @property
    def bulb_position(self) -> Tuple[int, int]:
        """Get the bulb position (first position)."""
        return self.positions[0]
    
    @property
    def top_position(self) -> Tuple[int, int]:
        """Get the top position (last position)."""
        return self.positions[-1]
    
    def __repr__(self) -> str:
        return f"Thermometer({self.id}, {self.positions})"


class ThermometerPuzzle:
    """
    Represents a Thermometers puzzle.

    The puzzle contains:
      - Row and column fill requirements
      - Thermometers to be filled
    """
    
    def __init__(
        self, 
        row_sums: List[int],
        col_sums: List[int], 
        thermometer_paths: List[List[Tuple[int, int]]]
    ):
        """
        Args:
            row_sums: Required filled cells per row
            col_sums: Required filled cells per column
            thermometer_paths: List of position lists, each defining a thermometer
        """
        if not row_sums or not col_sums:
            raise ValueError("Row and column sums cannot be empty")
        
        if any(s < 0 for s in row_sums) or any(s < 0 for s in col_sums):
            raise ValueError("All sums must be non-negative")
        
        if sum(row_sums) != sum(col_sums):
            raise ValueError("Sum of row sums must equal sum of column sums")
        
        self.height = len(row_sums)
        self.width = len(col_sums)
        self.row_sums = row_sums.copy()
        self.col_sums = col_sums.copy()
        
        # Validate sum constraints
        if any(s > self.width for s in row_sums):
            raise ValueError("Row sum cannot exceed grid width")
        
        if any(s > self.height for s in col_sums):
            raise ValueError("Column sum cannot exceed grid height")
        
        # Create thermometers
        if not thermometer_paths:
            raise ValueError("At least one thermometer path must be provided")
        
        self.thermometers = []
        for i, path in enumerate(thermometer_paths):
            if not path:
                raise ValueError(f"Thermometer path {i} is empty")
            self.thermometers.append(Thermometer(i, path))
        
        self._validate_grid_coverage()
    
    def _validate_grid_coverage(self) -> None:
        """Ensure grid is completely filled with non-overlapping thermometers."""
        all_positions = set()
        
        for thermo in self.thermometers:
            for pos in thermo.positions:
                row, col = pos
                
                # Check bounds
                if not (0 <= row < self.height and 0 <= col < self.width):
                    raise ValueError(f"Position {pos} outside grid bounds")
                
                # Check overlap
                if pos in all_positions:
                    raise ValueError(f"Position {pos} covered by multiple thermometers")
                
                all_positions.add(pos)
        
        # Check complete coverage
        expected_count = self.height * self.width
        if len(all_positions) != expected_count:
            raise ValueError(f"Grid not completely filled: {len(all_positions)}/{expected_count} cells covered")
    
    def is_valid_solution(self, filled_positions: Set[Tuple[int, int]]) -> bool:
        """Check if solution satisfies all constraints."""
        # Check thermometer fill constraints
        for thermo in self.thermometers:
            if not thermo.is_valid_fill_state(filled_positions):
                return False
        
        # Check row sums
        for row in range(self.height):
            actual = sum(1 for r, _ in filled_positions if r == row)
            if actual != self.row_sums[row]:
                return False
        
        # Check column sums
        for col in range(self.width):
            actual = sum(1 for _, c in filled_positions if c == col)
            if actual != self.col_sums[col]:
                return False
        
        return True
    
    def get_thermometer_at(self, position: Tuple[int, int]) -> Optional[Thermometer]:
        """Find which thermometer contains the given position."""
        for thermo in self.thermometers:
            if position in thermo.positions:
                return thermo
        return None
    
    def get_position_to_thermometer_map(self) -> dict[Tuple[int, int], Thermometer]:
        """Get a mapping from positions to their containing thermometers."""
        position_map = {}
        for thermo in self.thermometers:
            for pos in thermo.positions:
                position_map[pos] = thermo
        return position_map
    
    def __repr__(self) -> str:
        return f"ThermometerPuzzle({self.height}x{self.width}, {len(self.thermometers)} thermometers)"

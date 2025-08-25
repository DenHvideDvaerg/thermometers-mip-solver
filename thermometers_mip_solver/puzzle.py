from typing import List, Set, Tuple, Optional


def _horizontal_range(row: int, start_col: int, end_col: int) -> List[Tuple[int, int]]:
    """Generate a horizontal sequence of (row, col) tuples"""
    if start_col <= end_col:
        return [(row, col) for col in range(start_col, end_col + 1)]
    else:
        return [(row, col) for col in range(start_col, end_col - 1, -1)]


def _vertical_range(col: int, start_row: int, end_row: int) -> List[Tuple[int, int]]:
    """Generate a vertical sequence of (row, col) tuples"""
    if start_row <= end_row:
        return [(row, col) for row in range(start_row, end_row + 1)]
    else:
        return [(row, col) for row in range(start_row, end_row - 1, -1)]


def _create_thermometer_path(waypoints: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Create a thermometer path from a list of waypoints.
    
    Args:
        waypoints: List of (row, col) tuples representing key points in the thermometer path
        
    Returns:
        List of (row, col) tuples representing the complete thermometer path
        
    Raises:
        ValueError: If any two consecutive waypoints are not horizontally or vertically aligned,
                   or if the thermometer would have less than 2 cells
        
    Example:
        # For a thermometer that goes horizontally from (0,7) to (0,13)
        _create_thermometer_path([(0,7), (0,13)])
        # Returns: [(0,7), (0,8), (0,9), (0,10), (0,11), (0,12), (0,13)]
        
        # For an L-shaped thermometer: vertical then horizontal
        _create_thermometer_path([(2,0), (0,0), (0,3)])  
        # Returns: [(2,0), (1,0), (0,0), (0,1), (0,2), (0,3)]
    """
    if len(waypoints) < 2:
        raise ValueError("Thermometers must have at least 2 cells. Single-cell thermometers are not allowed.")
    
    path = [waypoints[0]]  # Start with the first waypoint
    
    for i in range(1, len(waypoints)):
        start_row, start_col = waypoints[i-1]
        end_row, end_col = waypoints[i]
        
        # Check if waypoints are aligned horizontally or vertically
        if start_row == end_row:
            # Horizontal segment
            if start_col != end_col:
                segment = _horizontal_range(start_row, start_col, end_col)[1:]  # Exclude start (already in path)
                path.extend(segment)
            # If start_col == end_col, it's the same point, so we don't add anything
        elif start_col == end_col:
            # Vertical segment
            if start_row != end_row:
                segment = _vertical_range(start_col, start_row, end_row)[1:]  # Exclude start (already in path)
                path.extend(segment)
            # If start_row == end_row, it's the same point, so we don't add anything
        else:
            # Not aligned horizontally or vertically - this is invalid for thermometers
            raise ValueError(f"Waypoints ({start_row},{start_col}) and ({end_row},{end_col}) are not horizontally or vertically aligned. Thermometers can only move in cardinal directions.")
    
    return path


class Thermometer:
    """
    Represents a thermometer as a sequence of connected cells.
    Mercury fills from the bulb (first position) towards the top.
    """
    
    def __init__(self, thermometer_id: int, waypoints: List[Tuple[int, int]]):
        """
        Args:
            thermometer_id: Unique identifier
            waypoints: List of (row, col) waypoints defining the thermometer path.
                      Waypoints will be expanded into a full path automatically.
        """
        if not waypoints:
            raise ValueError("Thermometer must have at least one waypoint")
        
        # Expand waypoints into full path
        self.positions = _create_thermometer_path(waypoints)
        
        if len(set(self.positions)) != len(self.positions):
            raise ValueError("Thermometer cannot have duplicate positions")
        
        self.id = thermometer_id
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
        thermometer_waypoints: List[List[Tuple[int, int]]]
    ):
        """
        Args:
            row_sums: Required filled cells per row
            col_sums: Required filled cells per column
            thermometer_waypoints: List of waypoint lists, each defining a thermometer 
                                 (waypoints will be expanded to full paths automatically)
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
        
        # Create thermometers from waypoints
        if not thermometer_waypoints:
            raise ValueError("At least one thermometer waypoints list must be provided")
        
        self.thermometers = []
        for i, waypoints in enumerate(thermometer_waypoints):
            if not waypoints:
                raise ValueError(f"Thermometer waypoints {i} is empty")
            self.thermometers.append(Thermometer(i, waypoints))

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
            # Calculated missing positions
            missing_positions = [
                (r, c) for r in range(self.height) for c in range(self.width)
                if (r, c) not in all_positions
            ]
            raise ValueError(f"Grid not completely filled: {len(all_positions)}/{expected_count} cells covered. Missing: {missing_positions}")

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

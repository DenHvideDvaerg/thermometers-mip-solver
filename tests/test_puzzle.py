import pytest
from thermometers_mip_solver import ThermometerPuzzle, Thermometer


class TestThermometer:
    """Test cases for the Thermometer class."""

    def test_basic_creation(self):
        """Test creating a basic thermometer."""
        positions = [(0, 0), (0, 1), (0, 2)]
        thermo = Thermometer(1, positions)
        
        assert thermo.id == 1
        assert thermo.positions == positions
        assert thermo.length == 3
        assert thermo.bulb_position == (0, 0)
        assert thermo.top_position == (0, 2)

    def test_single_cell_thermometer(self):
        """Test a thermometer with only one cell."""
        thermo = Thermometer(0, [(1, 1)])
        
        assert thermo.length == 1
        assert thermo.bulb_position == (1, 1)
        assert thermo.top_position == (1, 1)

    def test_empty_positions(self):
        """Test that empty positions raise ValueError."""
        with pytest.raises(ValueError, match="Thermometer must have at least one position"):
            Thermometer(1, [])

    def test_duplicate_positions(self):
        """Test that duplicate positions raise ValueError."""
        with pytest.raises(ValueError, match="Thermometer cannot have duplicate positions"):
            Thermometer(1, [(0, 0), (0, 1), (0, 0)])

    def test_non_adjacent_positions(self):
        """Test that non-adjacent positions raise ValueError."""
        # Gap between positions
        with pytest.raises(ValueError, match="Positions .* are not adjacent"):
            Thermometer(1, [(0, 0), (0, 2)])
        
        # Diagonal positions
        with pytest.raises(ValueError, match="Positions .* are not adjacent"):
            Thermometer(1, [(0, 0), (1, 1)])

    def test_valid_adjacent_positions(self):
        """Test various valid adjacent position patterns."""
        # Horizontal
        Thermometer(1, [(0, 0), (0, 1), (0, 2)])
        
        # Vertical
        Thermometer(2, [(2, 0), (1, 0), (0, 0)])
        
        # L-shaped
        Thermometer(3, [(2, 0), (1, 0), (1, 1), (1, 2)])
        
        # Snake pattern
        Thermometer(4, [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)])

    def test_valid_fill_states(self):
        """Test validation of thermometer fill states."""
        thermo = Thermometer(1, [(0, 0), (0, 1), (0, 2), (0, 3)])
        
        # Valid states: continuous from bulb
        assert thermo.is_valid_fill_state(set())  # Empty
        assert thermo.is_valid_fill_state({(0, 0)})  # Bulb only
        assert thermo.is_valid_fill_state({(0, 0), (0, 1)})  # First two
        assert thermo.is_valid_fill_state({(0, 0), (0, 1), (0, 2)})  # First three
        assert thermo.is_valid_fill_state({(0, 0), (0, 1), (0, 2), (0, 3)})  # All

    def test_invalid_fill_states(self):
        """Test invalid thermometer fill states."""
        thermo = Thermometer(1, [(0, 0), (0, 1), (0, 2), (0, 3)])
        
        # Invalid states
        assert not thermo.is_valid_fill_state({(0, 1)})  # Skip bulb
        assert not thermo.is_valid_fill_state({(0, 2)})  # Skip bulb and first
        assert not thermo.is_valid_fill_state({(0, 3)})  # Only top
        assert not thermo.is_valid_fill_state({(0, 0), (0, 2)})  # Gap in middle
        assert not thermo.is_valid_fill_state({(0, 0), (0, 1), (0, 3)})  # Gap at end

    def test_fill_state_with_unrelated_positions(self):
        """Test that unrelated filled positions don't affect validation."""
        thermo = Thermometer(1, [(0, 0), (0, 1)])
        
        # Valid fill with extra unrelated positions
        filled = {(0, 0), (1, 1), (2, 2)}  # Only (0,0) is from this thermometer
        assert thermo.is_valid_fill_state(filled)

    def test_repr(self):
        """Test string representation."""
        thermo = Thermometer(5, [(1, 2), (1, 3)])
        assert repr(thermo) == "Thermometer(5, [(1, 2), (1, 3)])"


class TestThermometerPuzzle:
    """Test cases for the ThermometerPuzzle class."""

    def test_basic_creation(self):
        """Test creating a basic puzzle."""
        puzzle = ThermometerPuzzle(
            row_sums=[1, 1],
            col_sums=[1, 1],
            thermometer_paths=[
                [(0, 0), (0, 1)],
                [(1, 1), (1, 0)]
            ]
        )
        
        assert puzzle.height == 2
        assert puzzle.width == 2
        assert len(puzzle.thermometers) == 2
        assert puzzle.row_sums == [1, 1]
        assert puzzle.col_sums == [1, 1]

    def test_empty_sums(self):
        """Test that empty row or column sums raise ValueError."""
        with pytest.raises(ValueError, match="Row and column sums cannot be empty"):
            ThermometerPuzzle([], [1], [[(0, 0)]])
        
        with pytest.raises(ValueError, match="Row and column sums cannot be empty"):
            ThermometerPuzzle([1], [], [[(0, 0)]])

    def test_negative_sums(self):
        """Test that negative sums raise ValueError."""
        with pytest.raises(ValueError, match="All sums must be non-negative"):
            ThermometerPuzzle([-1, 1], [1, 1], [[(0, 0)], [(0, 1)]])
        
        with pytest.raises(ValueError, match="All sums must be non-negative"):
            ThermometerPuzzle([1, 1], [1, -1], [[(0, 0)], [(0, 1)]])

    def test_mismatched_total_sums(self):
        """Test that mismatched row and column sum totals raise ValueError."""
        with pytest.raises(ValueError, match="Sum of row sums must equal sum of column sums"):
            ThermometerPuzzle([2], [1], [[(0, 0)]])

    def test_row_sum_exceeds_width(self):
        """Test that row sum exceeding grid width raises ValueError."""
        # Note: Need matching total sums first, then the row sum check will trigger
        with pytest.raises(ValueError, match="Row sum cannot exceed grid width"):
            ThermometerPuzzle([6], [3, 3], [[(0, 0)], [(0, 1)]])

    def test_col_sum_exceeds_height(self):
        """Test that column sum exceeding grid height raises ValueError."""
        # Note: Need matching total sums first, then the col sum check will trigger
        with pytest.raises(ValueError, match="Column sum cannot exceed grid height"):
            ThermometerPuzzle([2], [2, 0], [[(0, 0)], [(0, 1)]])  # height=1, but col sum 2 > 1

    def test_no_thermometer_paths(self):
        """Test that no thermometer paths raises ValueError."""
        with pytest.raises(ValueError, match="At least one thermometer path must be provided"):
            ThermometerPuzzle([1], [1], [])

    def test_empty_thermometer_path(self):
        """Test that empty thermometer path raises ValueError."""
        with pytest.raises(ValueError, match="Thermometer path 0 is empty"):
            ThermometerPuzzle([1], [1], [[]])

    def test_position_out_of_bounds(self):
        """Test that out-of-bounds positions raise ValueError."""
        # Position (0, 2) is outside 1x1 grid
        with pytest.raises(ValueError, match="Position .* outside grid bounds"):
            ThermometerPuzzle([1], [1], [[(0, 2)]])
        
        # Negative position
        with pytest.raises(ValueError, match="Position .* outside grid bounds"):
            ThermometerPuzzle([1], [1], [[(-1, 0)]])

    def test_overlapping_thermometers(self):
        """Test that overlapping thermometers raise ValueError."""
        with pytest.raises(ValueError, match="Position .* covered by multiple thermometers"):
            ThermometerPuzzle(
                [2, 0], [1, 1], 
                [
                    [(0, 0), (0, 1)], 
                    [(0, 1)]
                ]  # Both cover (0, 1)
            )

    def test_incomplete_grid_coverage(self):
        """Test that incomplete grid coverage raises ValueError."""
        with pytest.raises(ValueError, match="Grid not completely filled"):
            ThermometerPuzzle(
                [1, 1], [1, 1],
                [[(0, 0)]]  # Only covers 1 of 4 positions
            )

    def test_valid_solution_checking(self):
        """Test solution validation."""
        puzzle = ThermometerPuzzle(
            row_sums=[1, 2],
            col_sums=[2, 1],
            thermometer_paths=[
                [(1, 0), (0, 0)],  # Vertical thermometer
                [(1, 1), (0, 1)]   # Another vertical thermometer
            ]
        )
        
        # Valid solution: fill both bulbs and one top
        valid_solution = {(1, 0), (0, 0), (1, 1)}
        assert puzzle.is_valid_solution(valid_solution)
        
        # Invalid: wrong row sums
        invalid_row_sums = {(0, 0), (1, 1)} 
        assert not puzzle.is_valid_solution(invalid_row_sums)
        
        # Invalid: wrong column sums  
        invalid_col_sums = {(1, 0), (1, 1)}
        assert not puzzle.is_valid_solution(invalid_col_sums)
        
        # Invalid: thermometer fill violation (fill top without bulb)
        invalid_thermo = {(0, 0), (1, 1)}
        assert not puzzle.is_valid_solution(invalid_thermo)

    def test_get_thermometer_at(self):
        """Test finding thermometer at specific position."""
        puzzle = ThermometerPuzzle(
            [2], [1, 1],
            [[(0, 0), (0, 1)]]
        )
        
        thermo = puzzle.get_thermometer_at((0, 0))
        assert thermo is not None
        assert thermo.id == 0
        
        thermo = puzzle.get_thermometer_at((0, 1))
        assert thermo is not None  
        assert thermo.id == 0
        
        # Position not in puzzle
        assert puzzle.get_thermometer_at((1, 0)) is None

    def test_get_position_to_thermometer_map(self):
        """Test getting position to thermometer mapping."""
        puzzle = ThermometerPuzzle(
            [1, 1], [1, 1],
            [[(0, 0)], [(0, 1)], [(1, 0)], [(1, 1)]]
        )
        
        pos_map = puzzle.get_position_to_thermometer_map()
        
        assert len(pos_map) == 4
        assert pos_map[(0, 0)].id == 0
        assert pos_map[(0, 1)].id == 1
        assert pos_map[(1, 0)].id == 2
        assert pos_map[(1, 1)].id == 3

    def test_complex_puzzle(self):
        """Test with the real example."""
        puzzle = ThermometerPuzzle(
            row_sums=[1, 3, 2, 1],
            col_sums=[1, 2, 2, 2],
            thermometer_paths=[
                [(0, 2), (0, 1), (0, 0)],  
                [(0, 3), (1, 3)],
                [(1, 0), (2, 0)],
                [(1, 1), (1, 2)],
                [(2, 1), (2, 2), (2, 3)],
                [(3, 1), (3, 0)],
                [(3, 3), (3, 2)]
            ]
        )
        
        assert puzzle.height == 4
        assert puzzle.width == 4
        assert len(puzzle.thermometers) == 7
        
        # Test known valid solution
        solution = {(0, 3), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2), (3, 3)}
        assert puzzle.is_valid_solution(solution)

    def test_repr(self):
        """Test string representation."""
        puzzle = ThermometerPuzzle(
            [1], [1],
            [[(0, 0)]]
        )
        assert repr(puzzle) == "ThermometerPuzzle(1x1, 1 thermometers)"


class TestThermometerIntegration:
    """Integration tests for Thermometer and ThermometerPuzzle working together."""

    def test_thermometer_properties_in_puzzle(self):
        """Test that thermometer properties work correctly within puzzle context."""
        puzzle = ThermometerPuzzle(
            [2, 1], [1, 2],
            [[(0, 0), (0, 1), (1, 1)], [(1, 0)]]  # L-shaped thermometer + single cell to fill grid
        )
        
        thermo = puzzle.thermometers[0]
        assert thermo.length == 3
        assert thermo.bulb_position == (0, 0)
        assert thermo.top_position == (1, 1)
        
        # Test valid partial fills
        assert thermo.is_valid_fill_state({(0, 0)})  # Bulb only
        assert thermo.is_valid_fill_state({(0, 0), (0, 1)})  # First two
        assert thermo.is_valid_fill_state({(0, 0), (0, 1), (1, 1)})  # All
        
        # Test invalid fills
        assert not thermo.is_valid_fill_state({(0, 1)})  # Skip bulb
        assert not thermo.is_valid_fill_state({(1, 1)})  # Only top

    def test_puzzle_validation_catches_thermometer_errors(self):
        """Test that puzzle validation catches thermometer creation errors."""
        # Non-adjacent positions should be caught during thermometer creation
        with pytest.raises(ValueError, match="Positions .* are not adjacent"):
            ThermometerPuzzle(
                [1, 1], [1, 1],
                [[(0, 0), (1, 1)]]  # Diagonal positions
            )
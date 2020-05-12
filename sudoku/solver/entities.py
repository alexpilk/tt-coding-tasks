from typing import List, Set, Tuple


class Sudoku:
    SIZE = 9

    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.cells = {(i, j): Cell((i, j)) for j in range(self.SIZE) for i in range(self.SIZE)}

    def get_cell_value(self, coordinates: Tuple[int, int]) -> int:
        """
        Returns cell value from grid.
        """
        return self.grid[coordinates[1]][coordinates[0]]

    def get_row(self, row_index: int) -> List[int]:
        """
        Returns cell values from row.
        """
        return list(self.grid[row_index])

    @staticmethod
    def get_section_coordinates(coordinates: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns coordinates of cells located in the same 3x3 section as given cell.
        """
        section_id = (
            coordinates[0] // 3,
            coordinates[1] // 3,
        )
        coordinate_vector = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]
        for i, coordinate in enumerate(coordinate_vector):
            coordinate_vector[i] = (coordinate[0] + section_id[0] * 3, coordinate[1] + section_id[1] * 3)
        coordinate_vector.remove(coordinates)
        return coordinate_vector

    def enter(self, coordinates: Tuple[int, int], value: int) -> None:
        """
        Saves cell value.
        """
        self.grid[coordinates[1]][coordinates[0]] = value

    def get_cell_possible_values(self, coordinates: Tuple[int, int]) -> Set[int]:
        """
        Returns a set of possible values for cell if computed by searches.
        """
        cell = self.cells.get(coordinates)
        return set() if cell and self.get_cell_value(coordinates) else cell.possible_values


class Cell:

    def __init__(self, coordinates: Tuple[int, int]):
        self.coordinates = coordinates
        self.possible_values = set()

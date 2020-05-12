from abc import ABC, abstractmethod
from typing import List, Set, Tuple, Collection

from .entities import Sudoku, Cell


class BaseSearch(ABC):

    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    @abstractmethod
    def run(self, cell: Cell) -> Set[int]:
        """
        Returns possible values of given cell.
        """


class NeighborSearch(BaseSearch):
    """
    Takes values of neighbors along the horizontal and vertical axes, as well as within 3x3 sections
    and finds remaining possible values.
    """

    def run(self, cell: Cell) -> Set[int]:
        possible_values = set(range(1, 10))
        neighbors = self._collect_neighbors(cell.coordinates)
        return possible_values.difference(neighbors)

    def _collect_neighbors(self, coordinates: Tuple[int, int]) -> Set[int]:
        """
        Aggregates neighbors from horizontal and vertical axes, as well as 3x3 section.
        """
        horizontal = self._horizontal(coordinates)
        vertical = self._vertical(coordinates)
        section = self._section(coordinates)
        return horizontal.union(vertical).union(section)

    def _horizontal(self, coordinates: Tuple[int, int]) -> Set[int]:
        """
        Collects values of horizontal neighbors.
        """
        values = self.sudoku.get_row(coordinates[1])
        del values[coordinates[0]]
        return self._clear_zeroes(values)

    def _vertical(self, coordinates: Tuple[int, int]) -> Set[int]:
        """
        Collects values of vertical neighbors.
        """
        values = [self.sudoku.get_cell_value((coordinates[0], row)) for row in range(self.sudoku.SIZE)]
        del values[coordinates[1]]
        return self._clear_zeroes(values)

    def _section(self, coordinates: Tuple[int, int]) -> Set[int]:
        """
        Collects values of section neighbors.
        """
        coordinate_map = self.sudoku.get_section_coordinates(coordinates)
        result = {self.sudoku.get_cell_value(cell) for cell in coordinate_map}
        return self._clear_zeroes(result)

    @staticmethod
    def _clear_zeroes(values: Collection[int]) -> Set[int]:
        values = set(values)
        if 0 in values:
            values.remove(0)
        return values


class OptionSearch(BaseSearch):
    """
    Takes sets of possible values for each neighbor along the horizontal and vertical axes,
    as well as within 3x3 sections and finds unique possible options in given cell
    (missing from possible values of other neighbors).
    """

    def run(self, cell: Cell) -> Set[int]:
        option_vectors = self._get_options_for_each_vector(cell)
        if option_vectors:
            possible = set(range(1, 10))
            for options in option_vectors:
                possible = possible.intersection(options)
            return possible
        return cell.possible_values

    def _get_options_for_each_vector(self, cell: Cell) -> List[Set[int]]:
        """
        Finds unique option with regard to each type of neighbors (vertical, horizontal, section).
        """
        options_per_vector = [vector(cell.coordinates) for vector in [self._horizontal, self._vertical, self._section]]
        return [
            unique for options in options_per_vector if (unique := cell.possible_values.difference(options))
        ]

    def _horizontal(self, coordinates: Tuple[int, int]) -> Set[int]:
        """
        Collects possible values of horizontal neighbors.
        """
        coordinate_vector = [(i, coordinates[1]) for i in range(self.sudoku.SIZE)]
        coordinate_vector.remove(coordinates)
        return self._collect_options(coordinate_vector)

    def _vertical(self, coordinates: Tuple[int, int]) -> Set[int]:
        """
        Collects possible values of vertical neighbors.
        """
        coordinate_vector = [(coordinates[0], i) for i in range(self.sudoku.SIZE)]
        coordinate_vector.remove(coordinates)
        return self._collect_options(coordinate_vector)

    def _section(self, coordinates: Tuple[int, int]) -> Set[int]:
        """
        Collects possible values of section neighbors.
        """
        coordinate_map = self.sudoku.get_section_coordinates(coordinates)
        return self._collect_options(coordinate_map)

    def _collect_options(self, vector: List[Tuple[int, int]]) -> Set[int]:
        possible = set()
        for coord in vector:
            cell_possible_values = self.sudoku.get_cell_possible_values(coord)
            possible = possible.union(cell_possible_values)
        return possible

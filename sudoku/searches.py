from abc import ABC, abstractmethod


class BaseSearch(ABC):

    def __init__(self, sudoku):
        self.sudoku = sudoku

    @abstractmethod
    def run(self, cell):
        pass


class NeighborSearch(BaseSearch):

    def run(self, cell):
        possible_values = set(range(1, 10))
        neighbors = self._collect_neighbors(cell.coordinates)
        return possible_values.difference(neighbors)

    def _collect_neighbors(self, coord):
        horizontal = self._horizontal(coord)
        vertical = self._vertical(coord)
        section = self._section(coord)
        return horizontal.union(vertical).union(section)

    def _horizontal(self, coordinates):
        values = self.sudoku.get_row(coordinates[1])
        del values[coordinates[0]]
        return self._clear_zeroes(values)

    def _vertical(self, coordinates):
        values = [self.sudoku.get_cell((coordinates[0], row)) for row in range(self.sudoku.SIZE)]
        del values[coordinates[1]]
        return self._clear_zeroes(values)

    def _section(self, coordinates):
        coordinate_map = self.sudoku.get_section_coordinates(coordinates)
        result = {self.sudoku.get_cell(cell) for cell in coordinate_map}
        return self._clear_zeroes(result)

    @staticmethod
    def _clear_zeroes(values):
        values = set(values)
        if 0 in values:
            values.remove(0)
        return values


class OptionSearch(BaseSearch):

    def run(self, cell):
        option_vectors = self._get_options_for_each_vector(cell)
        if option_vectors:
            possible = set(range(1, 10))
            for options in option_vectors:
                possible = possible.intersection(options)
            return possible
        return cell.possible_values

    def _get_options_for_each_vector(self, cell):
        options_per_vector = [vector(cell.coordinates) for vector in [self._horizontal, self._vertical, self._section]]
        return [
            unique for options in options_per_vector if (unique := cell.possible_values.difference(options))
        ]

    def _horizontal(self, coordinates):
        coordinate_vector = [(i, coordinates[1]) for i in range(self.sudoku.SIZE)]
        coordinate_vector.remove(coordinates)
        return self._collect_options(coordinate_vector)

    def _vertical(self, coordinates):
        coordinate_vector = [(coordinates[0], i) for i in range(self.sudoku.SIZE)]
        coordinate_vector.remove(coordinates)
        return self._collect_options(coordinate_vector)

    def _section(self, coordinates):
        coordinate_map = self.sudoku.get_section_coordinates(coordinates)
        return self._collect_options(coordinate_map)

    def _collect_options(self, vector):
        possible = set()
        for coord in vector:
            cell_possible_values = self.sudoku.get_possible_values_from_cell(coord)
            possible = possible.union(cell_possible_values)
        return possible

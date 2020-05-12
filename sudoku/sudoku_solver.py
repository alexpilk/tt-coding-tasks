from copy import deepcopy

from searches import OptionSearch, NeighborSearch


def solve(sudoku):
    return Solver(Sudoku(sudoku)).solve()


class Solver:

    def __init__(self, sudoku):
        self.sudoku = sudoku

    def solve(self):
        starting_grid = deepcopy(self.sudoku.grid)

        while self._run_search(NeighborSearch):
            pass

        self._run_search(OptionSearch)

        return self.sudoku.grid if starting_grid == self.sudoku.grid else self.solve()

    def _run_search(self, search_type):
        for _, cell in self.sudoku.cells.items():
            if self.sudoku.get_cell(cell.coordinates) == 0:
                if self._try_solving_cell(search_type, cell):
                    return True
        return False

    def _try_solving_cell(self, search_type, cell):
        possible = search_type(self.sudoku).run(cell)
        cell.possible_values = possible
        return self._solve_cell(cell, possible)

    def _solve_cell(self, cell, possible):
        solved = len(possible) == 1
        if solved:
            self.sudoku.enter(cell.coordinates, list(possible)[0])
        return solved


class Sudoku:
    SIZE = 9

    def __init__(self, grid):
        self.grid = grid
        self.cells = {(i, j): Cell((i, j)) for j in range(self.SIZE) for i in range(self.SIZE)}

    def get_cell(self, coordinates):
        return self.grid[coordinates[1]][coordinates[0]]

    def get_row(self, row):
        return list(self.grid[row])

    def get_section_coordinates(self, coordinates):
        section_id = (
            coordinates[0] // 3,
            coordinates[1] // 3,
        )
        coordinate_map = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]
        for i, coordinate in enumerate(coordinate_map):
            coordinate_map[i] = (coordinate[0] + section_id[0] * 3, coordinate[1] + section_id[1] * 3)
        coordinate_map.remove(coordinates)
        return coordinate_map

    def enter(self, coordinates, value):
        self.grid[coordinates[1]][coordinates[0]] = value

    def get_possible_values_from_cell(self, coordinates):
        cell = self.cells.get(coordinates)
        return set() if cell and self.get_cell(coordinates) else cell.possible_values


class Cell:

    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.possible_values = set()

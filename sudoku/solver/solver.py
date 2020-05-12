from __future__ import annotations

from copy import deepcopy
from typing import List, Type, Set

from .entities import Sudoku, Cell
from .searches import OptionSearch, NeighborSearch, BaseSearch


def solve(sudoku: List[List[int]]) -> List[List[int]]:
    return Solver(Sudoku(sudoku)).solve()


class Solver:

    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    def solve(self) -> List[List[int]]:
        """
        Runs NeighborSearch until all easily computable cells are found.
        If OptionSearch doesn't solve any new cells - returns, otherwise repeats the process.
        """
        starting_grid = deepcopy(self.sudoku.grid)

        while self._run_search(NeighborSearch):
            pass

        self._run_search(OptionSearch)

        return self.sudoku.grid if starting_grid == self.sudoku.grid else self.solve()

    def _run_search(self, search_type: Type[BaseSearch]) -> bool:
        """
        Runs search for possible values on all unsolved cells.
        """
        for _, cell in self.sudoku.cells.items():
            if self.sudoku.get_cell_value(cell.coordinates) == 0:
                if self._try_solving_cell(search_type, cell):
                    return True
        return False

    def _try_solving_cell(self, search_type: Type[BaseSearch], cell: Cell) -> bool:
        """
        Runs search on given cell.
        """
        possible = search_type(self.sudoku).run(cell)
        cell.possible_values = possible
        return self._solve_cell(cell, possible)

    def _solve_cell(self, cell: Cell, possible: Set[int]) -> bool:
        """
        Enters value into given cell if only one value is possible.
        """
        solved = len(possible) == 1
        if solved:
            self.sudoku.enter(cell.coordinates, list(possible)[0])
        return solved

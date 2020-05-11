from typing import List, Tuple


class Board:

    def __init__(self, board: List[List[str]]):
        self.board = board

    def check_word(self, word: str) -> bool:
        """
        Checks whether the word is present on board.
        """
        starting_cells = self._find_starting_cells(word[0])

        return self._search(list(word[1:]), starting_cells)

    def _search(self, word: List[str], starting_cells: List[Tuple[int]], forbidden: List[Tuple[int]] = None) -> bool:
        """
        Recursively searches the board for next letters in the word.

        :param word: e.g. 'SEE'
        :param starting_cells: e.g. [(1, 0), (3, 2)]
        :param forbidden: cells already included in word that should not be revisited
        """
        forbidden = forbidden or []

        if not word:
            return True

        next_letter = word.pop(0)

        for cell in starting_cells:
            new_forbidden = forbidden + [cell]
            new_starting_cells = self._find_possible_cells(cell, next_letter, forbidden=new_forbidden)

            if not new_starting_cells:
                continue

            if self._search(list(word), new_starting_cells, new_forbidden):
                return True

        return False

    def _find_starting_cells(self, letter: str) -> List[Tuple[int]]:
        """
        Finds all cells containing starting letter of the word.
        """
        cells = []
        for row_index, row in enumerate(self.board):
            if letter in row:
                cells += [(row_index, i) for i, val in enumerate(row) if val == letter]
        return cells

    def _find_possible_cells(self, cell: Tuple[int], letter: str, forbidden: List[Tuple[int]]):
        """
        Checks given cell for adjacent cells containing given letter.

        :param cell: e.g. (1, 0)
        :param letter: e.g. 'S'
        :param forbidden: cells already included in word that should not be revisited
        :return: cells that are possible continuations of the route
        """
        adjacent_cells = self._adjacent_cells(cell)
        return [
            _cell for _cell in adjacent_cells if _cell not in forbidden and self._get_letter(_cell) == letter
        ]

    def _get_letter(self, cell: Tuple[int]) -> str:
        return self.board[cell[0]][cell[1]]

    def _adjacent_cells(self, cell: Tuple[int]) -> List[Tuple[int]]:
        """
        Returns coordinates of all adjacent cells.
        """
        offsets = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0)
        ]
        return [
            result for i, j in offsets if
            self._check_coordinates(result := (cell[0] + i, cell[1] + j))
        ]

    def _check_coordinates(self, cell: Tuple[int]) -> bool:
        """
        Checks if cell is within board dimensions.
        """
        return 0 <= cell[0] < len(self.board) and 0 <= cell[1] < len(self.board[0])

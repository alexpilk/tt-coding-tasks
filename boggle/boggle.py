class Board:

    def __init__(self, board):
        self.board = board

    def check_word(self, word):
        starting_points = self._find_starting_points(word[0])
        print(word[0], starting_points)
        if not starting_points:
            return False
        return self._process(list(word[1:]), starting_points)

    def _process(self, word, starting_points, forbidden=None):
        forbidden = forbidden or []

        if not word:
            return True

        next_letter = word.pop(0)
        for point in starting_points:
            new_forbidden = forbidden + [point]
            new_starting_points = self._find_next_letters(point, next_letter, forbidden=new_forbidden)
            print(next_letter, new_starting_points)
            if not new_starting_points:
                continue
            if self._process(list(word), new_starting_points, new_forbidden):
                return True

        return False

    def _find_starting_points(self, letter):
        coordinates = []
        for row_index, row in enumerate(self.board):
            if letter in row:
                coordinates += [(row_index, i) for i, val in enumerate(row) if val == letter]
        return coordinates

    def _find_next_letters(self, coordinates, letter, forbidden):
        possible_cells = [cell for cell in self._adjacent_cells(coordinates) if cell not in forbidden]
        return [cell for cell in possible_cells if self.board[cell[0]][cell[1]] == letter]

    def _adjacent_cells(self, coordinates):
        offsets = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0)
        ]
        return [
            (coordinates[0] + i, coordinates[1] + j) for i, j in offsets if
            self._check_coordinates((coordinates[0] + i, coordinates[1] + j))
        ]

    def _check_coordinates(self, coordinates):
        return 0 <= coordinates[0] < len(self.board) and 0 <= coordinates[1] < len(self.board[0])

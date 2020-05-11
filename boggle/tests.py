import pytest
from boggle import Board


@pytest.fixture
def board():
    return Board([
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ])


@pytest.mark.parametrize('word', ('ABCCED', 'SEE'))
def test_correct_word(board, word):
    assert board.check_word(word) is True


@pytest.mark.parametrize('word', ('ABCB',))
def test_incorrect_word(board, word):
    assert board.check_word(word) is False

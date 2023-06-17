import pytest

from pesto.board.board import Board
from pesto.board.perft import perft


@pytest.mark.perft
def test_perft_starting_position():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    node_count = perft(board=Board.from_fen(fen), depth=3)
    expected = {1: 20, 2: 400, 3: 8_902}
    assert node_count == expected

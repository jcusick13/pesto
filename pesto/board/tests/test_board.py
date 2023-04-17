from pytest_cases import parametrize_with_cases

from pesto.board.board import Board
from pesto.board.tests.test_board_cases import TestBoardFromFenCases


class TestBoard:
    @parametrize_with_cases(
        ("fen", "exp"),
        TestBoardFromFenCases,
    )
    def test_from_fen(self, fen: str, exp: Board):
        obs = Board.from_fen(fen)
        assert obs == exp

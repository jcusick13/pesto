import pytest
from pytest_cases import parametrize_with_cases

from pesto.board.board import Board
from pesto.board.tests.test_board_cases import (
    TestBoardFromFenCases,
    TestBoardToFenCases,
)


class TestBoard:
    @pytest.mark.unit
    @parametrize_with_cases(
        ("fen", "exp"),
        TestBoardFromFenCases,
    )
    def test_from_fen(self, fen: str, exp: Board):
        obs = Board.from_fen(fen)
        assert obs == exp

    @pytest.mark.unit
    @parametrize_with_cases(
        ("board", "exp"),
        TestBoardToFenCases,
    )
    def test_to_fen(self, board: Board, exp: str):
        obs = board.to_fen()
        assert obs == exp

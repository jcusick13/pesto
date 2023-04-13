from pytest_cases import parametrize_with_cases

from pesto.board.enums import Square
from pesto.board.piece import Bishop, Rook
from pesto.board.tests.test_piece_cases import (
    TestBishopPsuedoLegalMovesCases,
    TestRookPsuedoLegalMovesCases
)
from pesto.core.enums import Color

class TestBishop:
    @parametrize_with_cases(
        ("curr", "piece_set", "exp"),
        TestBishopPsuedoLegalMovesCases,
    )
    def test_generate_psuedo_legal_moves(
        self, curr: Square, piece_set: set[Square], exp: set[Square]
    ):
        obs = Bishop(color=Color.WHITE, curr=curr).generate_psuedo_legal_moves(
            piece_set=piece_set
        )
        assert obs == exp


class TestRook:
    @parametrize_with_cases(
        ("curr", "piece_set", "exp"),
        TestRookPsuedoLegalMovesCases,
    )
    def test_generate_psuedo_legal_moves(
        self, curr: Square, piece_set: set[Square], exp: set[Square]
    ):
        obs = Rook(color=Color.BLACK, curr=curr).generate_psuedo_legal_moves(
            piece_set=piece_set
        )
        assert obs == exp



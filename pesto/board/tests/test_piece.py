from pytest_cases import parametrize_with_cases

from pesto.board.enums import Square
from pesto.board.piece import Bishop, Knight, Rook, Queen, King
from pesto.board.tests.test_piece_cases import (
    TestBishopPsuedoLegalMovesCases,
    TestKingPsuedoLegalMovesCases,
    TestKnightPsuedoLegalMovesCases,
    TestRookPsuedoLegalMovesCases,
    TestQueenPsuedoLegalMovesCases,
)
from pesto.core.enums import Color


class TestKnight:
    @parametrize_with_cases(
        ("curr", "piece_set", "exp"),
        TestKnightPsuedoLegalMovesCases,
    )
    def test_generate_psuedo_legal_moves(
        self, curr: Square, piece_set: set[Square], exp: set[Square]
    ):
        obs = Knight(color=Color.BLACK, curr=curr).generate_psuedo_legal_moves(
            piece_set=piece_set
        )
        assert obs == exp


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


class TestQueen:
    @parametrize_with_cases(
        ("curr", "piece_set", "exp"),
        TestQueenPsuedoLegalMovesCases,
    )
    def test_generate_psuedo_legal_moves(
        self, curr: Square, piece_set: set[Square], exp: set[Square]
    ):
        obs = Queen(color=Color.WHITE, curr=curr).generate_psuedo_legal_moves(
            piece_set=piece_set
        )
        assert obs == exp


class TestKing:
    @parametrize_with_cases(
        ("curr", "piece_set", "exp"),
        TestKingPsuedoLegalMovesCases,
    )
    def test_generate_psuedo_legal_moves(
        self, curr: Square, piece_set: set[Square], exp: set[Square]
    ):
        obs = King(color=Color.BLACK, curr=curr).generate_psuedo_legal_moves(
            piece_set=piece_set
        )
        assert obs == exp

from typing import Optional

from pytest_cases import parametrize_with_cases

from pesto.board.piece import Bishop, King, Knight, Move, Pawn, Piece, Queen, Rook
from pesto.board.square import Square
from pesto.board.tests.test_piece_cases import (
    TestBishopPsuedoLegalMovesCases,
    TestKingPsuedoLegalMovesCases,
    TestKnightPsuedoLegalMovesCases,
    TestPawnPsuedoLegalMovesCases,
    TestQueenPsuedoLegalMovesCases,
    TestRookPsuedoLegalMovesCases,
)


class TestPawn:
    @parametrize_with_cases(
        ("pawn", "piece_map", "en_passant_sq", "exp"),
        TestPawnPsuedoLegalMovesCases,
    )
    def test_generate_psuedo_legal_moves(
        self,
        pawn: Pawn,
        piece_map: dict[Square, Piece],
        en_passant_sq: Optional[Square],
        exp: set[Move],
    ):
        obs = pawn.generate_psuedo_legal_moves(
            piece_map=piece_map, en_passant_sq=en_passant_sq
        )
        assert obs == exp


class TestKnight:
    @parametrize_with_cases(
        ("knight", "piece_map", "exp"),
        TestKnightPsuedoLegalMovesCases,
    )
    def test_generate_psuedo_legal_moves(
        self, knight: Knight, piece_map: dict[Square, Piece], exp: set[Move]
    ):
        obs = knight.generate_psuedo_legal_moves(piece_map=piece_map)
        assert obs == exp


class TestBishop:
    @parametrize_with_cases(
        ("bishop", "piece_map", "exp"),
        TestBishopPsuedoLegalMovesCases,
    )
    def test_generate_psuedo_legal_moves(
        self, bishop: Bishop, piece_map: dict[Square, Piece], exp: set[Move]
    ):
        obs = bishop.generate_psuedo_legal_moves(piece_map=piece_map)
        assert obs == exp


class TestRook:
    @parametrize_with_cases(
        ("rook", "piece_map", "exp"),
        TestRookPsuedoLegalMovesCases,
    )
    def test_generate_psuedo_legal_moves(
        self, rook: Rook, piece_map: dict[Square, Piece], exp: set[Move]
    ):
        obs = rook.generate_psuedo_legal_moves(piece_map=piece_map)
        assert obs == exp


class TestQueen:
    @parametrize_with_cases(
        ("queen", "piece_map", "exp"),
        TestQueenPsuedoLegalMovesCases,
    )
    def test_generate_psuedo_legal_moves(
        self, queen: Queen, piece_map: dict[Square, Piece], exp: set[Move]
    ):
        obs = queen.generate_psuedo_legal_moves(piece_map=piece_map)
        assert obs == exp


class TestKing:
    @parametrize_with_cases(
        ("king", "piece_map", "exp"),
        TestKingPsuedoLegalMovesCases,
    )
    def test_generate_psuedo_legal_moves(
        self, king: King, piece_map: dict[Square, Piece], exp: set[Move]
    ):
        obs = king.generate_psuedo_legal_moves(piece_map=piece_map)
        assert obs == exp

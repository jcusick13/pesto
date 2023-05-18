from typing import Optional

from pytest_cases import parametrize_with_cases

from pesto.board.move.castle import CastleRights
from pesto.board.move.legal import legal_move_generator
from pesto.board.move.apply import Move
from pesto.board.move.tests.test_legal_cases import TestLegalMoveGeneratorCases
from pesto.board.square import Square
from pesto.board.piece import Piece
from pesto.core.enums import Color


@parametrize_with_cases(
    ("piece_map", "castle_rights", "en_passant_sq", "to_move", "exp"),
    TestLegalMoveGeneratorCases,
)
def test_legal_move_generator(
    piece_map: dict[Square, Piece],
    castle_rights: CastleRights,
    en_passant_sq: Optional[Square],
    to_move: Color,
    exp: set[Move],
):
    obs = legal_move_generator(
        piece_map=piece_map,
        to_move=to_move,
        castle_rights=castle_rights,
        en_passant_sq=en_passant_sq,
    )
    assert sorted(obs) == sorted(exp)

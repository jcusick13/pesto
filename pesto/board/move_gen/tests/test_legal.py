from typing import Mapping, Optional

from pytest_cases import parametrize_with_cases

from pesto.board.move_gen.legal import legal_move_generator
from pesto.board.move_gen.moves import Move
from pesto.board.move_gen.tests.test_legal_cases import TestLegalMoveGeneratorCases
from pesto.board.square import Square
from pesto.board.piece import Piece
from pesto.core.enums import Color


@parametrize_with_cases(
    ("piece_map", "en_passant_sq", "to_move", "exp"),
    TestLegalMoveGeneratorCases,
)
def test_legal_move_generator(
    piece_map: Mapping[Square, Piece],
    en_passant_sq: Optional[Square],
    to_move: Color,
    exp: set[Move],
):
    obs = legal_move_generator(
        piece_map=piece_map, en_passant_sq=en_passant_sq, to_move=to_move
    )
    assert sorted(obs) == sorted(exp)

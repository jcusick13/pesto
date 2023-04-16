from typing import Mapping, Optional

from pytest_cases import parametrize_with_cases

from pesto.board.enums import Square
from pesto.board.piece import Piece
from pesto.board.move_gen.attack import square_is_attacked
from pesto.core.enums import Color
from pesto.board.move_gen.tests.test_attack_cases import TestSquareIsAttackedCases


@parametrize_with_cases(
    ("square", "piece_map", "by", "exp"),
    TestSquareIsAttackedCases,
)
def test_square_is_attacked(
    square: Square, piece_map: Mapping[Square, Piece], by: Optional[Color], exp: bool
):
    obs = square_is_attacked(square=square, piece_map=piece_map, by=by)
    assert exp == obs

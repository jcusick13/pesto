from typing import Optional

import pytest
from pytest_cases import parametrize_with_cases

from pesto.board.move.attack import square_is_attacked
from pesto.board.move.tests.test_attack_cases import TestSquareIsAttackedCases
from pesto.board.piece import Piece
from pesto.board.square import Square
from pesto.core.enums import Color


@pytest.mark.unit
@parametrize_with_cases(
    ("square", "piece_map", "by", "exp"),
    TestSquareIsAttackedCases,
)
def test_square_is_attacked(
    square: Square, piece_map: dict[Square, Piece], by: Optional[Color], exp: bool
):
    obs = square_is_attacked(piece_map=piece_map, square=square, by=by)
    assert exp == obs

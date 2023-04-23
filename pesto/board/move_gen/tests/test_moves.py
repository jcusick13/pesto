from typing import Mapping

import pytest
from pytest_cases import parametrize_with_cases

from pesto.board.move_gen.moves import Move, make_move, unmake_move
from pesto.board.move_gen.tests.test_moves_cases import (
    TestMakeMoveCases,
    TestUnmakeMoveCases,
)
from pesto.board.square import Square
from pesto.board.piece import King, Pawn, Piece
from pesto.core.enums import Color


@parametrize_with_cases(
    ("in_piece_map", "in_move", "out_piece_map", "out_move", "exception"),
    TestMakeMoveCases,
)
def test_make_move(
    in_piece_map: Mapping[Square, Piece],
    in_move: Move,
    out_piece_map: Mapping[Square, Piece],
    out_move: Move,
    exception: bool,
):
    if exception:
        with pytest.raises(ValueError):
            _, _ = make_move(in_piece_map, in_move)

    else:
        obs_piece_map, obs_move = make_move(in_piece_map, in_move)
        assert obs_piece_map == out_piece_map
        assert obs_move == out_move


@parametrize_with_cases(
    ("in_piece_map", "in_move", "out_piece_map", "exception"),
    TestUnmakeMoveCases,
)
def test_unmake_move(
    in_piece_map: Mapping[Square, Piece],
    in_move: Move,
    out_piece_map: Mapping[Square, Piece],
    exception: bool,
):
    if exception:
        with pytest.raises(ValueError):
            _ = unmake_move(in_piece_map, in_move)

    else:
        obs_piece_map = unmake_move(in_piece_map, in_move)
        assert obs_piece_map == out_piece_map


def test_make_and_unmake_move():
    """Ensure `piece_map` is unchanged after making and
    reverting a move
    """
    starting_piece_map = {
        Square.E4: King(Color.BLACK, Square.E4),
        Square.E5: Pawn(Color.WHITE, Square.E5),
    }
    input_move = Move(
        piece=King(Color.BLACK, Square.E4),
        start=Square.E4,
        end=Square.E5,
    )
    piece_map, move = make_move(starting_piece_map, input_move)
    ending_piece_map = unmake_move(piece_map, move)

    assert starting_piece_map == ending_piece_map

from typing import Optional

import pytest
from pytest_cases import parametrize_with_cases

from pesto.board.board_state import (
    find_en_passant_target,
    update_castle_rights,
    update_halfmove_clock,
)
from pesto.board.move.castle import CastleRights
from pesto.board.piece import Move
from pesto.board.square import Square
from pesto.board.tests.test_board_state_cases import (
    FindEnPassantTargetCases,
    UpdateCastleRightsCases,
    UpdateHalfmoveClockCases,
)


@pytest.mark.unit
@parametrize_with_cases(
    ("move", "exp"),
    FindEnPassantTargetCases,
)
def test_find_en_passant_target(move: Move, exp: Optional[Square]):
    obs = find_en_passant_target(move=move)
    assert obs == exp


@pytest.mark.unit
@parametrize_with_cases(
    ("castle_rights", "move", "exp"),
    UpdateCastleRightsCases,
)
def test_update_castle_rights(
    castle_rights: CastleRights, move: Move, exp: CastleRights
):
    obs = update_castle_rights(castle_rights=castle_rights, move=move)
    assert obs == exp


@pytest.mark.unit
@parametrize_with_cases(
    ("clock", "move", "exp"),
    UpdateHalfmoveClockCases,
)
def test_update_halfmove_clock(clock: int, move: Move, exp: int):
    obs = update_halfmove_clock(clock=clock, move=move)
    assert obs == exp

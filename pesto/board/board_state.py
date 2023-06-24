# pylint: disable=too-many-return-statements, too-many-branches
from copy import deepcopy
from typing import Optional

from pesto.board.move.castle import CastleRights, CastleSide
from pesto.board.piece import CastlingMove, King, Move, Pawn, Rook, SinglePieceMove
from pesto.board.square import Square
from pesto.core.enums import Color


def find_en_passant_target(move: Move) -> Optional[Square]:
    """Returns a square eligible to be attacked via
    en passant after the passed move has been played
    """
    if not isinstance(move.start, Pawn):
        return None

    move_dist: int = abs(move.start.curr.value - move.end.curr.value)
    if move_dist != 32:
        return None

    # Pawn moved two squares
    direction: int = 1 if move.start.color == Color.WHITE else -1
    ep_square_idx: int = move.end.curr.value - 16 * direction
    return Square(ep_square_idx)


def update_castle_rights(castle_rights: CastleRights, move: Move) -> CastleRights:
    """Returns a new CastlingRights object based upon
    the provided move
    """
    short_rook_sq = {Square.H1, Square.H8}
    long_rook_sq = {Square.A1, Square.A8}
    side: CastleSide

    castle_rights_ = deepcopy(castle_rights)

    if isinstance(move, SinglePieceMove):
        if isinstance(move.captures, Rook) and move.captures.curr in (
            short_rook_sq | long_rook_sq
        ):
            if move.captures.curr in long_rook_sq:
                side = CastleSide.LONG
            else:
                side = CastleSide.SHORT
            castle_rights_.set_false(color=move.captures.color, castle_side=side)
            return castle_rights_

        if not isinstance(move.start, (Rook, King)):
            return castle_rights_

        if isinstance(move.start, King):
            castle_rights_.set_false(
                color=move.start.color, castle_side=CastleSide.SHORT
            )
            castle_rights_.set_false(
                color=move.start.color, castle_side=CastleSide.LONG
            )
            return castle_rights_

        if isinstance(move.start, Rook):
            if move.start.curr not in (short_rook_sq | long_rook_sq):
                return castle_rights_

            if move.start.curr in long_rook_sq:
                side = CastleSide.LONG
            else:
                side = CastleSide.SHORT

            castle_rights_.set_false(color=move.start.color, castle_side=side)
            return castle_rights_

    if isinstance(move, CastlingMove):
        if move.castled_rook.start.curr in long_rook_sq:
            side = CastleSide.LONG
        else:
            side = CastleSide.SHORT

        castling_color = move.start.color
        if not castle_rights_(castling_color)[side]:
            raise ValueError(f"{castling_color} has no rights to castle {side.value}")

        castle_rights_.set_false(castling_color, CastleSide.SHORT)
        castle_rights_.set_false(castling_color, CastleSide.LONG)
        return castle_rights_

    return castle_rights_


def update_halfmove_clock(clock: int, move: Move) -> int:
    """Determines the new value of the halfmove clock
    based on the provided move
    """
    if isinstance(move, CastlingMove):
        return clock + 1

    if isinstance(move.start, Pawn) or move.captures is not None:
        return 0

    return clock + 1

from typing import Optional

from pesto.board.move.castle import CastleRights, CastleSide
from pesto.board.piece import CastlingMove, Move, Pawn
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
    """Returns an updated CastlingRights object based upon
    the provided move
    """
    if not isinstance(move, CastlingMove):
        return castle_rights

    side: CastleSide
    if move.castled_rook.start.curr.value % 16 == 0:
        # Rook started on the a-file
        side = CastleSide.LONG
    else:
        side = CastleSide.SHORT

    castling_color = move.start.color
    if not castle_rights(castling_color)[side]:
        raise ValueError(f"{castling_color} has no rights to castle {side.value}")

    castle_rights.flip(color=castling_color, castle_side=side)
    return castle_rights


def update_halfmove_clock(clock: int, move: Move) -> int:
    """Determines the new value of the halfmove clock
    based on the provided move
    """
    if isinstance(move, CastlingMove):
        return clock + 1

    if isinstance(move.start, Pawn) or move.captures is not None:
        return 0

    return clock + 1

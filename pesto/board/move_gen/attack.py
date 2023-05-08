from typing import Mapping, Optional

from pesto.board.square import Square
from pesto.board.piece import Piece
from pesto.core.enums import Color


def square_is_attacked(
    piece_map: Mapping[Square, Piece],
    square: Square,
    by: Optional[Color] = None,
) -> bool:
    """Determines if `square` is attacked by any pieces on
    the board.

    piece_map: Locations of all pieces on the board
    square: Location to check if under attack
    by: When `Color` is provided, check only if that `Color`
        attacks `square`
    """
    for _, piece in piece_map.items():
        if by is not None and piece.color != by:
            continue

        moves = piece.generate_psuedo_legal_moves(piece_map=piece_map)
        attacked_squares: set[Square] = {move.end.curr for move in moves}
        if square in attacked_squares:
            return True

    return False

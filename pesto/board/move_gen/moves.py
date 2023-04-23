from copy import deepcopy
from dataclasses import dataclass
from typing import Mapping, Optional

from pesto.board.square import Square
from pesto.board.piece import Piece


@dataclass
class Move:
    piece: Piece
    start: Square
    end: Square
    captures: Optional[Piece] = None


def make_move(
    piece_map: Mapping[Square, Piece], move: Move
) -> tuple[Mapping[Square, Piece], Move]:
    """Creates and returns a new `piece_map` based on the
    given `move` to be played.
    """
    _piece_map = deepcopy(piece_map)
    _move = deepcopy(move)

    if (piece := _piece_map.pop(_move.start, None)) is None:
        raise ValueError(f"Could not find piece on {_move.start} to move")

    if piece != _move.piece:
        raise ValueError(
            "Discrepancy between provided piece and what was found on that square"
        )

    # Remove captured piece
    if (captured_piece := _piece_map.pop(_move.end, None)) is not None:
        if captured_piece.color == _move.piece.color:
            raise ValueError("Attempted to capture piece of same color")
    _move.captures = captured_piece

    # Update moved piece internals and place it on the board
    _move.piece.curr = _move.end
    _piece_map[_move.end] = _move.piece

    return _piece_map, _move


def unmake_move(
    piece_map: Mapping[Square, Piece], move: Move
) -> Mapping[Square, Piece]:
    """Creates and returns a new `piece_map` based on
    reverting the provided `move`
    """
    _piece_map = deepcopy(piece_map)
    _move = deepcopy(move)

    if _piece_map.get(_move.start) is not None:
        raise ValueError("Could not revert move, as existing piece was found on square")

    if _move.captures is not None:
        if (piece := _piece_map.get(_move.end)) is None:
            raise ValueError(
                f"Expected to find {_move.piece} on {_move.end}, but found None"
            )

        if piece != _move.piece:
            raise ValueError(
                f"Expected to find {_move.piece} on {_move.end}, but found {piece}"
            )
        # Add back captured piece
        _piece_map[_move.end] = _move.captures

    else:
        # Empty square of any piece
        _piece_map.pop(_move.end, None)

    # Update reverted piece internals and place it on the board
    _move.piece.curr = _move.start
    _piece_map[_move.start] = _move.piece

    return _piece_map

from copy import deepcopy
from typing import Optional

from pesto.board.piece import CastlingMove, Move, Piece, SinglePieceMove
from pesto.board.square import Square


def make_move(
    piece_map: dict[Square, Piece], move: Move
) -> tuple[dict[Square, Piece], Move]:
    """Creates and returns a new `piece_map` based on the
    given `move` to be played.
    """
    _piece_map: dict[Square, Piece] = deepcopy(piece_map)

    if (start_piece := _piece_map.pop(move.start.curr, None)) is None:
        raise ValueError(f"Could not find piece on {move.start.curr} to move")

    if start_piece != move.start:
        raise ValueError(
            "Discrepancy between provided piece and what was found on that square"
        )

    _move: Move
    if isinstance(move, SinglePieceMove):
        captured_piece: Optional[Piece] = None

        # Check for captures found from looking on the board
        if (observed_capture := _piece_map.pop(move.end.curr, None)) is not None:
            if observed_capture.color == move.end.color:
                raise ValueError("Attempted to capture piece of same color")
            captured_piece = observed_capture

        # Check for captures from provided `move` object
        if (provided_capture := move.captures) is not None:
            if provided_capture.color == move.end.color:
                raise ValueError("Attempted to capture piece of same color")

            if _piece_map.pop(provided_capture.curr, None) is None:
                raise ValueError(
                    f"Provided capture, {provided_capture} is not found on the board"
                )
            captured_piece = provided_capture

        _move = SinglePieceMove(start=move.start, end=move.end, captures=captured_piece)

        # Update piece map to reflect having moved the piece
        _piece_map[_move.end.curr] = _move.end

    elif isinstance(move, CastlingMove):
        if (rook_to_move := _piece_map.pop(move.castled_rook.start.curr, None)) is None:
            raise ValueError(
                f"Could not find rook on {move.castled_rook.start.curr} to move"
            )

        if rook_to_move != move.castled_rook.start:
            raise ValueError(
                "Discrepancy between rook to move and what was found on that square"
            )

        _piece_map[move.end.curr] = move.end
        _piece_map[move.castled_rook.end.curr] = move.castled_rook.end
        _move = deepcopy(move)

    else:
        raise TypeError(f"Unknown move type provided: {type(move)}")

    return _piece_map, _move


def unmake_move(piece_map: dict[Square, Piece], move: Move) -> dict[Square, Piece]:
    """Creates and returns a new `piece_map` based on
    reverting the provided `move`.

    Considers reverting both the "main" piece (i.e. the piece
    described in `move.start`) the the "captured" piece (i.e.
    the piece described in `move.captures`)
    """
    _piece_map = deepcopy(piece_map)
    _move = deepcopy(move)

    if _piece_map.get(_move.start.curr) is not None:
        raise ValueError("Could not revert move, as existing piece was found on square")

    if _piece_map.get(_move.end.curr) != move.end:
        raise ValueError(
            "Could not revert move, as the main piece was not found on the end square"
        )

    # Clear the square where the main piece landed
    _piece_map.pop(_move.end.curr, None)

    if isinstance(_move, SinglePieceMove):
        if _move.captures is not None:
            # Add captured piece back to it's original location
            _piece_map[_move.captures.curr] = _move.captures

    elif isinstance(_move, CastlingMove):
        # Reset the rook to it's original location
        _piece_map.pop(_move.castled_rook.end.curr)
        _piece_map[_move.castled_rook.start.curr] = _move.castled_rook.start

    else:
        raise TypeError(f"Unknown move type provided: {type(_move)}")

    # Update piece map to put the original piece back in it's starting place
    _piece_map[_move.start.curr] = _move.start

    return _piece_map

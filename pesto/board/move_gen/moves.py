from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Mapping, Optional

from pesto.board.board import CastleRights, CastleSide
from pesto.board.move_gen.attack import square_is_attacked
from pesto.board.square import Square
from pesto.board.piece import King, Piece, Rook
from pesto.core.enums import Color


@dataclass
class Move:
    piece: Piece
    start: Square
    end: Square
    captures: Optional[Piece] = None

    def __lt__(self, other: Move) -> bool:
        return (self.start.value + self.end.value) < (
            other.start.value + other.end.value
        )


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


@dataclass
class CastleSquare:
    """Container for identifying king and rook square
    locations before and after castling
    """

    color: Color
    castle_side: CastleSide

    def __post_init__(self):
        self._color_adjust: int = 0 if self.color == Color.WHITE else 112

    @property
    def passthrough_squares(self) -> list[Square]:
        """Squares the king and rook pass through"""
        passthrough_idx_map = {CastleSide.SHORT: [5, 6], CastleSide.LONG: [1, 2, 3]}
        squares: list[Square] = []
        for square_idx in passthrough_idx_map[self.castle_side]:
            squares.append(Square(square_idx + self._color_adjust))
        return squares

    @property
    def rook_start(self) -> Square:
        """Rook location before castling"""
        rook_start_idx_map = {CastleSide.SHORT: 7, CastleSide.LONG: 0}
        return Square(rook_start_idx_map[self.castle_side] + self._color_adjust)

    @property
    def rook_end(self) -> Square:
        """Rook location after castling"""
        rook_end_idx_map = {CastleSide.SHORT: 5, CastleSide.LONG: 3}
        return Square(rook_end_idx_map[self.castle_side] + self._color_adjust)

    @property
    def king_start(self) -> Square:
        """King locaton before castling"""
        return Square(4 + self._color_adjust)

    @property
    def king_end(self) -> Square:
        """King location after castling"""
        king_end_idx_map = {CastleSide.SHORT: 6, CastleSide.LONG: 2}
        return Square(king_end_idx_map[self.castle_side] + self._color_adjust)


def generate_castling_moves(
    piece_map: Mapping[Square, Piece],
    castle_rights: CastleRights,
    to_move: Color,
) -> list[Move]:
    """Return a list of castling move objects if the side `to_move`
    is legally allowed to castle in either direction
    """
    moves: list[Move] = []
    opposite_color: Color = Color.WHITE if to_move == Color.BLACK else Color.BLACK
    rights: dict[CastleSide, bool] = castle_rights(color=to_move)

    for castling_side in CastleSide:
        able_to_castle: bool = True

        if rights[castling_side] is True:
            squares = CastleSquare(color=to_move, castle_side=castling_side)

            # Check that no pieces are between king and rook
            for square in squares.passthrough_squares:
                if piece_map.get(square) is not None:
                    able_to_castle = False
                    break

            if not able_to_castle:
                continue

            # Check if the king passes through check
            for square in squares.passthrough_squares:
                if square_is_attacked(
                    piece_map=piece_map, square=square, by=opposite_color
                ):
                    able_to_castle = False
                    break

            if not able_to_castle:
                continue

            # Able to castle! Add king and rook moves to return list
            king: King = piece_map[squares.king_start]
            rook: Rook = piece_map[squares.rook_start]
            moves.append(
                Move(piece=king, start=squares.king_start, end=squares.king_end)
            )
            moves.append(
                Move(piece=rook, start=squares.rook_start, end=squares.rook_end)
            )

    return moves

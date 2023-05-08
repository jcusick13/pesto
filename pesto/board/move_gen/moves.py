from copy import deepcopy
from dataclasses import dataclass
from typing import Mapping

from pesto.board.board import CastleRights, CastleSide
from pesto.board.move_gen.attack import square_is_attacked
from pesto.board.square import Square
from pesto.board.piece import King, Move, Piece, Rook
from pesto.core.enums import Color


def make_move(
    piece_map: Mapping[Square, Piece], move: Move
) -> tuple[Mapping[Square, Piece], Move]:
    """Creates and returns a new `piece_map` based on the
    given `move` to be played.
    """
    _piece_map = deepcopy(piece_map)

    if (piece := _piece_map.pop(move.start.curr, None)) is None:
        raise ValueError(f"Could not find piece on {move.start.curr} to move")

    if piece != move.start:
        raise ValueError(
            "Discrepancy between provided piece and what was found on that square"
        )

    # Remove captured piece
    if (captured_piece := _piece_map.pop(move.end.curr, None)) is not None:
        if captured_piece.color == move.end.color:
            raise ValueError("Attempted to capture piece of same color")
    _move = Move(start=move.start, end=move.end, captures=captured_piece)

    # Update piece map to reflect having moved the piece
    _piece_map[_move.end.curr] = _move.end

    return _piece_map, _move


def unmake_move(
    piece_map: Mapping[Square, Piece], move: Move
) -> Mapping[Square, Piece]:
    """Creates and returns a new `piece_map` based on
    reverting the provided `move`
    """
    _piece_map = deepcopy(piece_map)
    _move = deepcopy(move)

    if _piece_map.get(_move.start.curr) is not None:
        raise ValueError("Could not revert move, as existing piece was found on square")

    if _move.captures is not None:
        if (piece := _piece_map.get(_move.end.curr)) is None:
            raise ValueError(
                f"Expected to find {_move.end.type} on {_move.end.curr}, but found None"
            )

        if piece != _move.end:
            raise ValueError(
                f"Expected to find {_move.end.type} on {_move.end.curr}, "
                f"but found {piece}"
            )
        # Add back captured piece
        _piece_map[_move.end.curr] = _move.captures

    else:
        # Empty square of any piece
        _piece_map.pop(_move.end.curr, None)

    # Update piece mpa to reflect having moved the piece
    _piece_map[_move.start.curr] = _move.start

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
            moves.append(
                Move(
                    start=King(color=to_move, curr=squares.king_start),
                    end=King(color=to_move, curr=squares.king_end),
                )
            )
            moves.append(
                Move(
                    start=Rook(color=to_move, curr=squares.rook_start),
                    end=Rook(color=to_move, curr=squares.rook_end),
                )
            )

    return moves

# pylint: disable=too-many-branches
from __future__ import annotations

from abc import abstractmethod, abstractproperty
from dataclasses import dataclass
from typing import Optional, Mapping, Union

from pesto.board.square import Square
from pesto.board.utils import index_on_board
from pesto.core.enums import Color, PieceType


DIAG_OFFSETS: set[int] = {-15, -17, 15, 17}
VERT_HORIZ_OFFSETS: set[int] = {-16, -1, 16, 1}


@dataclass(eq=True, frozen=True)
class BasePiece:
    color: Color
    curr: Square

    @property
    @abstractproperty
    def type(self) -> PieceType:
        pass

    @classmethod
    @abstractmethod
    def new(cls, color: Color, curr: Square) -> BasePiece:
        pass


@dataclass(eq=True, frozen=True)
class NonPawnPiece(BasePiece):
    @property
    @abstractproperty
    def _slides(self) -> bool:
        """Is the piece a sliding piece (queen, rook, bishop) or
        not (knight and king only make one hop)"""

    @property
    @abstractproperty
    def _offsets(self) -> set[int]:
        """Contains offsets required for the possible locations
        of a piece's next move"""

    def generate_psuedo_legal_moves(
        self, piece_map: Mapping[Square, BasePiece]
    ) -> set[Move]:
        """Create set of moves which only consider the movement
        rules of a piece along with the placement of other
        pieces on the board.
        """
        moves: set[Square] = set()
        start_square: Square = self.curr

        for offset in self._offsets:
            blocked: bool = False
            square: Square = self.curr

            while not blocked:
                if not index_on_board(square.value + offset):
                    break

                square = Square(square.value + offset)
                if (piece := piece_map.get(square)) is not None:
                    if piece.color != self.color:
                        moves.add(
                            Move(
                                start=self.new(self.color, start_square),
                                end=self.new(self.color, square),
                            )
                        )
                    break

                moves.add(
                    Move(
                        start=self.new(self.color, start_square),
                        end=self.new(self.color, square),
                    )
                )
                if not self._slides:
                    break

        return moves


class Pawn(BasePiece):
    # To be set to False after having moved
    is_first_move: bool = True

    @property
    def type(self) -> PieceType:
        return PieceType.PAWN

    @classmethod
    def new(cls, color: Color, curr: Square, is_first_move: bool = True) -> Pawn:
        pawn = Pawn(color, curr)
        if is_first_move:
            return pawn

        pawn.is_first_move = False
        return pawn

    def generate_psuedo_legal_moves(
        self,
        piece_map: Mapping[Square, BasePiece],
    ) -> set[Move]:
        """Create set of moves which only consider the movement
        rules of a pawn along with the placement of other
        pieces on the board.
        """
        direction = 1 if self.color == Color.WHITE else -1
        start_square: Square = self.curr
        moves: set[Move] = set()
        next_idx: int
        capture_idx: int

        # Check one square forward
        next_idx = self.curr.value + (16 * direction)
        if index_on_board(next_idx):
            if Square(next_idx) not in piece_map:
                moves.add(
                    Move(
                        start=self.new(
                            self.color,
                            curr=start_square,
                            is_first_move=self.is_first_move,
                        ),
                        end=self.new(
                            self.color, curr=Square(next_idx), is_first_move=False
                        ),
                    )
                )

        # Check two squares forward
        if self.is_first_move:
            next_idx = self.curr.value + (2 * 16 * direction)
            if index_on_board(next_idx):
                if Square(next_idx) not in piece_map:
                    moves.add(
                        Move(
                            start=self.new(
                                self.color,
                                curr=start_square,
                                is_first_move=self.is_first_move,
                            ),
                            end=self.new(
                                self.color, curr=Square(next_idx), is_first_move=False
                            ),
                        )
                    )

        # Check capture left
        capture_idx = self.curr.value + (15 * direction)
        if index_on_board(capture_idx):
            if (piece := piece_map.get(Square(capture_idx))) is not None:
                if piece.color != self.color:
                    moves.add(
                        Move(
                            start=self.new(
                                self.color,
                                curr=start_square,
                                is_first_move=self.is_first_move,
                            ),
                            end=self.new(
                                self.color,
                                curr=Square(capture_idx),
                                is_first_move=False,
                            ),
                        )
                    )

        # Check capture right
        capture_idx = self.curr.value + (17 * direction)
        if index_on_board(capture_idx):
            if (piece := piece_map.get(Square(capture_idx))) is not None:
                if piece.color != self.color:
                    moves.add(
                        Move(
                            start=self.new(
                                self.color,
                                curr=start_square,
                                is_first_move=self.is_first_move,
                            ),
                            end=self.new(
                                self.color,
                                curr=Square(capture_idx),
                                is_first_move=False,
                            ),
                        )
                    )

        return moves


class Knight(NonPawnPiece):
    @property
    def type(self) -> PieceType:
        return PieceType.KNIGHT

    @property
    def _slides(self) -> bool:
        return False

    @property
    def _offsets(self) -> set[int]:
        return {-33, -18, 14, 31, 33, 18, -14, -31}

    @classmethod
    def new(cls, color: Color, curr: Square) -> Knight:
        return Knight(color, curr)


class Bishop(NonPawnPiece):
    @property
    def type(self) -> PieceType:
        return PieceType.BISHOP

    @property
    def _slides(self) -> bool:
        return True

    @property
    def _offsets(self) -> set[int]:
        return DIAG_OFFSETS

    @classmethod
    def new(cls, color: Color, curr: Square) -> Bishop:
        return Bishop(color, curr)


class Rook(NonPawnPiece):
    @property
    def type(self) -> PieceType:
        return PieceType.ROOK

    @property
    def _slides(self) -> bool:
        return True

    @property
    def _offsets(self) -> set[int]:
        return VERT_HORIZ_OFFSETS

    @classmethod
    def new(cls, color: Color, curr: Square) -> Rook:
        return Rook(color, curr)


class Queen(NonPawnPiece):
    @property
    def type(self) -> PieceType:
        return PieceType.QUEEN

    @property
    def _slides(self) -> bool:
        return True

    @property
    def _offsets(self) -> set[int]:
        return DIAG_OFFSETS | VERT_HORIZ_OFFSETS

    @classmethod
    def new(cls, color: Color, curr: Square) -> Queen:
        return Queen(color, curr)


class King(NonPawnPiece):
    @property
    def type(self) -> PieceType:
        return PieceType.KING

    @property
    def _slides(self) -> bool:
        return False

    @property
    def _offsets(self) -> set[int]:
        return DIAG_OFFSETS | VERT_HORIZ_OFFSETS

    @classmethod
    def new(cls, color: Color, curr: Square) -> King:
        return King(color, curr)


Piece = Union[Pawn, Knight, Bishop, Rook, Queen, King]


@dataclass(eq=True, frozen=True)
class Move:
    start: Piece
    end: Piece
    captures: Optional[Piece] = None

    def __lt__(self, other: Move) -> bool:
        return (self.start.curr.value + self.end.curr.value) < (
            other.start.curr.value + other.end.curr.value
        )

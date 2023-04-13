from abc import abstractmethod, abstractproperty
from dataclasses import dataclass
from typing import Mapping

from pesto.board.enums import Square
from pesto.core.enums import Color, PieceType


DIAG_OFFSETS: set[int] = {-15, -17, 15, 17}
VERT_HORIZ_OFFSETS: set[int] = {-16, -1, 16, 1}


@dataclass
class BasePiece:
    color: Color
    curr: Square

    @property
    @abstractproperty
    def type(self) -> PieceType:
        pass

    @property
    @abstractproperty
    def _slides(self) -> bool:
        """Is the piece a sliding piece (queen, rook, bishop) or
        not (knight and king only make one hop)"""
        pass

    @abstractmethod
    def _offsets(self, **kwargs) -> set[int]:
        """Contains offsets required for the possible locations
        of a piece's next move"""
        pass

    def generate_psuedo_legal_moves(
        self, piece_set: set[Square]
    ) -> set[Square]:
        """Create set of moves which only consider the movement
        rules of a piece along with the placement of other
        pieces on the board.

        piece_set: Contains squares which have a piece on them
        """
        moves: set[Square] = set()

        for offset in self._offsets():
            blocked: bool = False
            square: Square = self.curr

            while not blocked:
                if (square.value + offset) & 0x88 != 0:
                    break
                square = Square(square.value + offset)

                if square in piece_set:
                    break

                moves.add(square)

                if not self._slides:
                    break

        return moves


class Pawn(BasePiece):
    @property
    def type(self) -> PieceType:
        return PieceType.PAWN

    @property
    def _slides(self) -> bool:
        return False

    def _offsets(self, **kwargs) -> set[int]:
        return set()

    def generate_psuedo_legal_moves(
        self, piece_set: set[Square]
    ) -> set[Square]:
        return set()


class Knight(BasePiece):
    @property
    def type(self) -> PieceType:
        return PieceType.KNIGHT

    @property
    def _slides(self) -> bool:
        return False

    def _offsets(self, **kwargs) -> set[int]:
        return {-33, -18, 14, 31, 33, 18, -14, -31}


class Bishop(BasePiece):
    @property
    def type(self) -> PieceType:
        return PieceType.BISHOP

    @property
    def _slides(self) -> bool:
        return True

    def _offsets(self, **kwargs) -> set[int]:
        return DIAG_OFFSETS



class Rook(BasePiece):
    @property
    def type(self) -> PieceType:
        return PieceType.ROOK

    @property
    def _slides(self) -> bool:
        return True

    def _offsets(self, **kwargs) -> set[int]:
        return VERT_HORIZ_OFFSETS

class Queen(BasePiece):
    @property
    def type(self) -> PieceType:
        return PieceType.QUEEN

    @property
    def _slides(self) -> bool:
        return True

    def _offsets(self, **kwargs) -> set[int]:
        return DIAG_OFFSETS | VERT_HORIZ_OFFSETS


class King(BasePiece):
    @property
    def type(self) -> PieceType:
        return PieceType.KING

    @property
    def _slides(self) -> bool:
        return False

    def _offsets(self, **kwargs) -> set[int]:
        return DIAG_OFFSETS | VERT_HORIZ_OFFSETS

# pylint: disable=too-many-branches
from abc import abstractproperty
from dataclasses import dataclass

from pesto.board.enums import Square
from pesto.board.utils import index_on_board
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


@dataclass
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

    def generate_psuedo_legal_moves(self, piece_set: set[Square]) -> set[Square]:
        """Create set of moves which only consider the movement
        rules of a piece along with the placement of other
        pieces on the board.

        piece_set: Contains squares which have a piece on them
        """
        moves: set[Square] = set()

        for offset in self._offsets:
            blocked: bool = False
            square: Square = self.curr

            while not blocked:
                if not index_on_board(square.value + offset):
                    break
                square = Square(square.value + offset)
                moves.add(square)

                if square in piece_set:
                    break

                if not self._slides:
                    break

        return moves


class Pawn(BasePiece):
    # To be set to False after having moved
    is_first_move: bool = True

    @property
    def type(self) -> PieceType:
        return PieceType.PAWN

    def generate_psuedo_legal_moves(
        self,
        piece_set: set[Square],
    ) -> set[Square]:
        """Create set of moves which only consider the movement
        rules of a pawn along with the placement of other
        pieces on the board.

        piece_set: Contains squares which have a piece on them
        """
        direction = 1 if self.color == Color.WHITE else -1
        moves: set[Square] = set()
        next_idx: int
        capture_idx: int

        # Check one square forward
        next_idx = self.curr.value + (16 * direction)
        if index_on_board(next_idx):
            if Square(next_idx) not in piece_set:
                moves.add(Square(next_idx))

        # Check two squares forward
        if self.is_first_move:
            next_idx = self.curr.value + (2 * 16 * direction)
            if index_on_board(next_idx):
                if Square(next_idx) not in piece_set:
                    moves.add(Square(next_idx))

        # Check capture left
        capture_idx = self.curr.value + (15 * direction)
        if index_on_board(capture_idx):
            if Square(capture_idx) in piece_set:
                moves.add(Square(capture_idx))

        # Check capture right
        capture_idx = self.curr.value + (17 * direction)
        if index_on_board(capture_idx):
            if Square(capture_idx) in piece_set:
                moves.add(Square(capture_idx))

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


Piece = tuple[Pawn, Knight, Bishop, Rook, Queen, King]

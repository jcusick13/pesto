from typing import Optional

from pesto.board.move.castle import CastleRights, CastleSide
from pesto.board.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from pesto.board.square import Square, str_to_square
from pesto.core.enums import Color


def dump_castling_rights_to_fen(castle_rights: CastleRights) -> str:
    """Converts a `CastleRights` object to it's portion
    of a FEN string
    """
    castle_string = ""
    if castle_rights(Color.WHITE)[CastleSide.SHORT]:
        castle_string += "K"
    if castle_rights(Color.WHITE)[CastleSide.LONG]:
        castle_string += "Q"
    if castle_rights(Color.BLACK)[CastleSide.SHORT]:
        castle_string += "k"
    if castle_rights(Color.WHITE)[CastleSide.LONG]:
        castle_string += "q"

    if castle_string == "":
        return "-"

    return castle_string


def dump_en_passant_target_to_fen(square: Optional[Square]) -> str:
    """Converts a possible en passant target square to
    it's portion of a FEN string
    """
    if square is None:
        return "-"

    return square.name.lower()


def dump_piece_map_to_fen(piece_map: dict[Square, Piece]) -> str:
    """Converts a piece map representation of a board into
    it's portion of a FEN string
    """
    board_string = ""
    letter_map = {
        Bishop: "B",
        King: "K",
        Knight: "N",
        Pawn: "P",
        Queen: "Q",
        Rook: "R",
    }

    for rank_idx in range(7, -1, -1):
        rank_string = ""
        empty_squares = 0

        for file_idx in range(0, 8):
            piece = piece_map.get(Square((rank_idx * 16) + file_idx))

            if piece is None:
                empty_squares += 1
                continue

            char = letter_map[type(piece)]
            char = char.lower() if piece.color == Color.BLACK else char

            if empty_squares > 0:
                # Add the count of previous empty squares now
                # that we've found a non-empty square
                char = str(empty_squares) + char
                empty_squares = 0

            rank_string += char

        # Ensure ranks ending in empty squares (or entirely
        # empty ranks) have their empty sqaure count added
        if empty_squares > 0:
            rank_string += str(empty_squares)

        if rank_idx != 0:
            rank_string += "/"

        board_string += rank_string

    return board_string


def parse_fen_piece_map(string: str) -> dict[Square, Piece]:
    """Maps the piece location string segment of a FEN string
    into a piece map
    """
    piece_map: dict[Square, Piece] = {}
    letter_map = {
        "B": Bishop,
        "K": King,
        "N": Knight,
        "P": Pawn,
        "Q": Queen,
        "R": Rook,
    }

    ranks = string.split("/")
    rank_idx: int
    pieces: str
    for rank_idx, pieces in enumerate(reversed(ranks)):
        file_idx = 0
        piece: str
        for piece in pieces:
            if piece.isdigit():
                file_idx += int(piece)
                continue

            color = Color.WHITE if piece.isupper() else Color.BLACK
            square = Square((rank_idx * 16) + file_idx)
            piece_map[square] = letter_map[piece.upper()].new(
                color=color,
                curr=square,
            )
            file_idx += 1

    return piece_map


def parse_fen_en_passant_target(string: str) -> Optional[Square]:
    """Maps the en passant string segment of a FEN string into
    a `Square`, if one is present
    """
    if string == "-":
        return None

    return str_to_square(string)


def parse_fen_castling_rights(string: str) -> CastleRights:
    """Maps the castling string segment of a FEN string into
    a `CastleRights` object
    """
    castle_rights = CastleRights(
        _rights={
            Color.WHITE: {CastleSide.SHORT: False, CastleSide.LONG: False},
            Color.BLACK: {CastleSide.SHORT: False, CastleSide.LONG: False},
        }
    )
    if string == "-":
        return castle_rights

    char_map: dict[str, tuple[Color, CastleSide]] = {
        "K": (Color.WHITE, CastleSide.SHORT),
        "Q": (Color.WHITE, CastleSide.LONG),
        "k": (Color.BLACK, CastleSide.SHORT),
        "q": (Color.BLACK, CastleSide.LONG),
    }
    for char in string:
        color, castle_side = char_map[char]
        castle_rights.flip(color, castle_side)

    return castle_rights

#include <vector>
#include "collections.h"
#include "exceptions.h"

CastleRights::CastleRights() {
  kingside = true;
  queenside = true;
}

CastleRights::CastleRights(bool kingside_, bool queenside_)
  : kingside(kingside_), queenside(queenside_) {};


bool CastleRights::operator==(const CastleRights &other) const {
  bool kings_equal = other.kingside == kingside;
  bool queens_equal = other.queenside == queenside;
  return kings_equal & queens_equal;
}
 
Pieces::Pieces() {
  // Initialize object to an empty board
  _pawns = std::make_unique<std::vector<U64>>(2);
  _pawns->at(WHITE) = 0ULL;
  _pawns->at(BLACK) = 0ULL;

  _knights = std::make_unique<std::vector<U64>>(2);
  _knights->at(WHITE) = 0ULL;
  _knights->at(BLACK) = 0ULL;

  _bishops = std::make_unique<std::vector<U64>>(2);
  _bishops->at(WHITE) = 0ULL;
  _bishops->at(BLACK) = 0ULL;

  _rooks = std::make_unique<std::vector<U64>>(2);
  _rooks->at(WHITE) = 0ULL;
  _rooks->at(BLACK) = 0ULL;

  _queens = std::make_unique<std::vector<U64>>(2);
  _queens->at(WHITE) = 0ULL;
  _queens->at(BLACK) = 0ULL;

  _kings = std::make_unique<std::vector<U64>>(2);
  _kings->at(WHITE) = 0ULL;
  _kings->at(BLACK) = 0ULL;
};

void Pieces::initStartingPosition() {
  U64 white_pawns = 0b11111111 << 8;
  U64 black_pawns = white_pawns << (8 * 5);
  _pawns->at(WHITE) = white_pawns;
  _pawns->at(BLACK) = black_pawns;

  U64 white_knights = 0b01000010;
  U64 black_knights = white_knights << (8 * 7);
  _knights->at(WHITE) = white_knights;
  _knights->at(BLACK) = black_knights;

  U64 white_bishops = 0b00100100;
  U64 black_bishops = white_bishops << (8 * 7);
  _bishops->at(WHITE) = white_bishops;
  _bishops->at(BLACK) = black_bishops;

  U64 white_rooks = 0b10000001;
  U64 black_rooks = white_rooks << (8 * 7);
  _rooks->at(WHITE) = white_rooks;
  _rooks->at(BLACK) = black_rooks;

  U64 white_queen = 0b00001000;
  U64 black_queen = white_queen << (8 * 7);
  _queens->at(WHITE) = white_queen;
  _queens->at(BLACK) = black_queen;

  U64 white_king = 0b00010000;
  U64 black_king = white_king << (8 * 7);
  _kings->at(WHITE) = white_king;
  _kings->at(BLACK) = black_king;
}

bb_vec* Pieces::get(PieceType piece_type) {
  switch (piece_type) {
    case PAWN:
      return _pawns.get();

    case KNIGHT:
      return _knights.get();

    case BISHOP:
      return _bishops.get();

    case ROOK:
      return _rooks.get();

    case QUEEN:
      return _queens.get();

    case KING:
      return _kings.get();

    default:
      throw InvalidPieceException();
  }
}

U64 Pieces::getColor(Color color) {
  U64 bb = 0ULL;
  return (
    bb | _pawns->at(color) | _knights->at(color) |
    _bishops->at(color) | _rooks->at(color) |
    _queens->at(color) | _kings->at(color)
  );
}

U64 Pieces::occupied() {
  U64 bb = 0ULL;
  return (
    bb | _pawns->at(WHITE) | _pawns->at(BLACK) |
    _knights->at(WHITE) | _knights->at(BLACK) |
    _bishops->at(WHITE) | _bishops->at(BLACK) |
    _rooks->at(WHITE) | _rooks->at(BLACK) |
    _queens->at(WHITE) | _queens->at(BLACK) |
    _kings->at(WHITE) | _kings->at(BLACK)
  ) ;
}


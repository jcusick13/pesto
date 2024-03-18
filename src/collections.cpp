#include <vector>
#include "collections.h"

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
  pawns = {0ULL, 0ULL};
  knights = {0ULL, 0ULL};
  bishops = {0ULL, 0ULL};
  rooks = {0ULL, 0ULL};
  queens = {0ULL, 0ULL};
  kings = {0ULL, 0ULL};
};

void Pieces::initStartingPosition() {
  U64 white_pawns = 0b11111111 << 8;
  U64 black_pawns = white_pawns << (8 * 5);
  pawns[WHITE] = white_pawns;
  pawns[BLACK] = black_pawns;

  U64 white_knights = 0b01000010;
  U64 black_knights = white_knights << (8 * 7);
  knights[WHITE] = white_knights;
  knights[BLACK] = black_knights;

  U64 white_bishops = 0b00100100;
  U64 black_bishops = white_bishops << (8 * 7);
  bishops[WHITE] = white_bishops;
  bishops[BLACK] = black_bishops;

  U64 white_rooks = 0b10000001;
  U64 black_rooks = white_rooks << (8 * 7);
  rooks[WHITE] = white_rooks;
  rooks[BLACK] = black_rooks;

  U64 white_queen = 0b00001000;
  U64 black_queen = white_queen << (8 * 7);
  queens[WHITE] = white_queen;
  queens[BLACK] = black_queen;

  U64 white_king = 0b00010000;
  U64 black_king = white_king << (8 * 7);
  kings[WHITE] = white_king;
  kings[BLACK] = black_king;
}


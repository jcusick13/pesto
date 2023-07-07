#include <bit>
#include <cstdint>

#include "board.h"

// Initialize board to the start of a new game
Board::Board()
{
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

  U64 white_queen = 0b00010000;
  U64 black_queen = white_queen << (8 * 7);
  queens[WHITE] = white_queen;
  queens[BLACK] = black_queen;

  U64 white_king = 0b00001000;
  U64 black_king = white_king << (8 * 7);
  kings[WHITE] = white_king;
  kings[BLACK] = black_king;
};


// Find the least significant non-zero bit. Flip it and 
// return it's index
Square popLeastSigBit(U64 &piece_bb)
{
  int first_non_zero_idx = std::countr_zero(piece_bb);
  piece_bb &= ~(1ULL << first_non_zero_idx);

  return Square(first_non_zero_idx);
};


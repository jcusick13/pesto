#include <bitset>
#include <cstdint>
#include <string>
#include <vector>

#include <gtest/gtest.h>

#include "board.h"

using namespace std;

/*
  XORing bits of piece type for each color should
  be the 16 bits of the first/last two ranks for
  a starting game position
*/
TEST(BoardConstructorTest, StartingPosition)
{
  Board board = Board();

  U64 white = (
    board.pawns  [WHITE] ^=
    board.knights[WHITE] ^=
    board.bishops[WHITE] ^=
    board.rooks  [WHITE] ^=
    board.queens [WHITE] ^=
    board.kings  [WHITE]
  );
  U64 exp_white = 0b1111111111111111;
  EXPECT_EQ(white, exp_white);

  U64 black = (
    board.pawns  [BLACK] ^=
    board.knights[BLACK] ^=
    board.bishops[BLACK] ^=
    board.rooks  [BLACK] ^=
    board.queens [BLACK] ^=
    board.kings  [BLACK]
  );
  U64 exp_black = exp_white << (8 * 6);
  EXPECT_EQ(black, exp_black) << board.pawns[BLACK]; 
};


/*
  Confirm that a bitboard with a single bit flipped
  can be returned as a square, and that the bit is
  reset to zero
*/
TEST(PopLeastSigBitTest, BitboardWithSingleSquare)
{
  U64 bb_a1 = 1ULL;
  Square obs_sq_1 = popLeastSigBit(bb_a1);
  Square exp_sq_1 = a1;
  EXPECT_EQ(obs_sq_1, exp_sq_1) << "Failed to return square a1";
  EXPECT_EQ(bb_a1, 0ULL) << "Failed to flip a1 bit";

  U64 bb_h1 = 1ULL << h1;
  Square obs_sq_2 = popLeastSigBit(bb_h1);
  Square exp_sq_2 = h1;
  EXPECT_EQ(obs_sq_2, exp_sq_2) << "Failed for square h1";
  EXPECT_EQ(bb_h1, 0ULL) << "Failed to flip h1 bit";

  U64 bb_c4 = 1ULL << c4;
  Square obs_sq_3 = popLeastSigBit(bb_c4);
  Square exp_sq_3 = c4;
  EXPECT_EQ(obs_sq_3, exp_sq_3) << "Failed for square c4";
  EXPECT_EQ(bb_c4, 0ULL) << "Failed to flip c4 bit";

  U64 bb_h8 = 1ULL << h8;
  Square obs_sq_4 = popLeastSigBit(bb_h8);
  Square exp_sq_4 = h8;
  EXPECT_EQ(obs_sq_4, exp_sq_4) << "Failed for square h8";
  EXPECT_EQ(bb_h8, 0ULL) << "Failed to flip h8 bit";
};


/*
  Confirm a single bitboard with multiple bits
  flipped can have it's squares repeatedly popped
  until the board is empty
*/
TEST(PopLeastSigBitTest, BitboardWithMultipleSquares)
{
  // Create bitboard with three bits flipped
  U64 board = 0ULL;
  vector<Square> squares = {a5, c2, f6};
  for (Square s : squares){
    U64 bb_sq = 1ULL << s;
    board |= bb_sq;
  }

  vector<Square> lsb_squares;
  for (Square s : squares){
    Square sq = popLeastSigBit(board);
    lsb_squares.push_back(sq);
  }

  set<Square> exp_squares = set<Square>(squares.begin(), squares.end());
  set<Square> obs_squares = set<Square>(lsb_squares.begin(), lsb_squares.end());
  EXPECT_EQ(board, 0ULL);
};

#include <gtest/gtest.h>

#include "board.h"

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


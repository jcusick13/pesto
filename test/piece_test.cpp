#include <string>
#include <vector>

#include <gtest/gtest.h>

#include "piece.h"

using namespace std;


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

/*
  Confirm single square movement in all directions
*/
TEST(NorthOneTest, CenterOfBoard)
{
  U64 bb_single_piece = 1ULL << d4;
  EXPECT_EQ(northOne(bb_single_piece), 1ULL << d5);

  U64 bb_multi_piece = 1ULL << c3 | 1ULL << g7;
  EXPECT_EQ(northOne(bb_multi_piece), 1ULL << c4 | 1ULL << g8);
}

TEST(NorthOneTest, TopOfBoard)
{
  U64 bb_single_piece = 1ULL << a8;
  EXPECT_EQ(northOne(bb_single_piece), 0ULL);

  U64 bb_multi_piece = 1ULL << d7 | 1ULL << f8;
  EXPECT_EQ(northOne(bb_multi_piece), 1ULL << d8);
}


TEST(SouthOneTest, CenterOfBoard)
{
  U64 bb_single_piece = 1ULL << h4;
  EXPECT_EQ(southOne(bb_single_piece), 1ULL << h3);

  U64 bb_multi_piece = 1ULL << c6 | 1ULL << f8;
  EXPECT_EQ(southOne(bb_multi_piece), 1ULL << c5 | 1ULL << f7);
}

TEST(SouthOneTest, BottomOfBoard)
{
  U64 bb_single_piece = 1ULL << c1;
  EXPECT_EQ(southOne(bb_single_piece), 0ULL);

  U64 bb_multi_piece = 1ULL << e1 | 1ULL << f2;
  EXPECT_EQ(southOne(bb_multi_piece), 1ULL << f1);
}


TEST(EastOneTest, CenterOfBoard)
{
  U64 bb_single_piece = 1ULL << b7;
  EXPECT_EQ(eastOne(bb_single_piece), 1ULL << c7);

  U64 bb_multi_piece = 1ULL << d2 | 1ULL << f8;
  EXPECT_EQ(eastOne(bb_multi_piece), 1ULL << e2 | 1ULL << g8);
}

TEST(EastOneTest, RightOfBoard)
{
  U64 bb_single_piece = 1ULL << h2;
  EXPECT_EQ(eastOne(bb_single_piece), 0ULL);

  U64 bb_multi_piece = 1ULL << h8 | 1ULL << f6;
  EXPECT_EQ(eastOne(bb_multi_piece), 1ULL << g6);
}


TEST(WestOneTest, CenterOfBoard)
{
  U64 bb_single_piece = 1ULL << e3;
  EXPECT_EQ(westOne(bb_single_piece), 1ULL << d3);

  U64 bb_multi_piece = 1ULL << b6 | 1ULL << h2;
  EXPECT_EQ(westOne(bb_multi_piece), 1ULL << a6 | 1ULL << g2);
}

TEST(WestOneTest, LeftOfBoard)
{
  U64 bb_single_piece = 1ULL << a6;
  EXPECT_EQ(westOne(bb_single_piece), 0ULL);

  U64 bb_multi_piece = 1ULL << a4 | 1ULL << b8;
  EXPECT_EQ(westOne(bb_multi_piece), 1ULL << a8);
}


TEST(NorthEastOneTest, CenterOfBoard)
{
  U64 bb_single_piece = 1ULL << d4;
  EXPECT_EQ(northEastOne(bb_single_piece), 1ULL << e5);
  
  U64 bb_multi_piece = 1ULL << a1 | 1ULL << g5;
  EXPECT_EQ(northEastOne(bb_multi_piece), 1ULL << b2 | 1ULL << h6);
}

TEST(NorthEastOneTest, TopRightOfBoard)
{
  U64 bb_single_piece = 1ULL << h8;
  EXPECT_EQ(northEastOne(bb_single_piece), 0ULL);

  U64 bb_multi_piece = 1ULL << a8 | 1ULL << h1 | 1ULL << g5;
  EXPECT_EQ(northEastOne(bb_multi_piece), 1ULL << h6);
}


TEST(SouthEastOneTest, CenterOfBoard)
{
  U64 bb_single_piece = 1ULL << c7;
  EXPECT_EQ(southEastOne(bb_single_piece), 1ULL << d6);

  U64 bb_multi_piece = 1ULL << e4 | 1ULL << f7;
  EXPECT_EQ(southEastOne(bb_multi_piece), 1ULL << f3 | 1ULL << g6);
}

TEST(SouthEastOneTest, BottomRightOfBoard)
{
  U64 bb_single_piece = 1ULL << h1;
  EXPECT_EQ(southEastOne(bb_single_piece), 0ULL);

  U64 bb_multi_piece = 1ULL << a1 | 1ULL << h5 | 1ULL << b8;
  EXPECT_EQ(southEastOne(bb_multi_piece), 1ULL << c7);
}


TEST(SouthWestOneTest, CenterOfBoard)
{
  U64 bb_single_piece = 1ULL << g4;
  EXPECT_EQ(southWestOne(bb_single_piece), 1ULL << f3);

  U64 bb_multi_piece = 1ULL << c3 | 1ULL << h8;
  EXPECT_EQ(southWestOne(bb_multi_piece), 1ULL << b2 | 1ULL << g7);
}

TEST(SouthWestOneTest, BottomLeftOfBoard)
{
  U64 bb_single_piece = 1ULL << a1;
  EXPECT_EQ(southWestOne(bb_single_piece), 0ULL);

  U64 bb_multi_piece = 1ULL << a8 | 1ULL << f1 | 1ULL << b4;
  EXPECT_EQ(southWestOne(bb_multi_piece), 1ULL << a3);
}


TEST(NorthWestOneTest, CenterOfBoard)
{
  U64 bb_single_piece = 1ULL << f4;
  EXPECT_EQ(northWestOne(bb_single_piece), 1ULL << e5);

  U64 bb_multi_piece = 1ULL << b3 | 1ULL << d6;
  EXPECT_EQ(northWestOne(bb_multi_piece), 1ULL << a4 | 1ULL << c7);
}

TEST(NorthWestOneTest, TopLeftOfBoard)
{
  U64 bb_single_piece = 1ULL << a8;
  EXPECT_EQ(northWestOne(bb_single_piece), 0ULL);

  U64 bb_multi_piece = 1ULL << a4 | 1ULL << e8 | 1ULL << g3;
  EXPECT_EQ(northWestOne(bb_multi_piece), 1ULL << f4);
}


/*
  Confirm Knight movement from center of the board
*/
TEST(GetKnightAttacksTest, CenterOfBoard)
{
  U64 knight_bb = 1ULL << d4;
  U64 attacks = getKnightAttacks(knight_bb);

  U64 exp_bb = (
    1ULL << e6 | 1ULL << f5 | 1ULL << f3 | 1ULL << e2 |
    1ULL << c2 | 1ULL << b3 | 1ULL << b5 | 1ULL << c6
  );
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetKnightAttacksTest, TopRightOfBoard)
{
  U64 knight_bb = 1ULL << g7;
  U64 attacks = getKnightAttacks(knight_bb);

  U64 exp_bb = 1ULL << h5 | 1ULL << f5 | 1ULL << e6 | 1ULL << e8;
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetKnightAttacksTest, BottomLeftOfBoard)
{
  U64 knight_bb = 1ULL << a3;
  U64 attacks = getKnightAttacks(knight_bb);

  U64 exp_bb = 1ULL << b5 | 1ULL << c4 | 1ULL << c2 | 1ULL << b1;
  EXPECT_EQ(attacks, exp_bb);
}


/*
  Confirm King movement from the center of the board
*/
TEST(GetKingAttacksTest, CenterOfBoard)
{
  U64 king_bb = 1ULL << d4;
  U64 attacks = getKingAttacks(king_bb);

  U64 exp_bb = (
    1ULL << c4 | 1ULL << c5 | 1ULL << d5 | 1ULL << e5 |
    1ULL << e4 | 1ULL << e3 | 1ULL << d3 | 1ULL << c3
  );
  EXPECT_EQ(attacks, exp_bb);
};


/*
  Confirm King movement from side of the board
*/
TEST(GetKingAttacksTest, SideOfBoard)
{
  U64 king_bb = 1ULL << h5;
  U64 attacks = getKingAttacks(king_bb);

  U64 exp_bb = 1ULL << h6 | 1ULL << g6 | 1ULL << g5 | 1ULL << g4 | 1ULL << h4;
  EXPECT_EQ(attacks, exp_bb);
};

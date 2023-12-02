#include <string>
#include <vector>

#include <gtest/gtest.h>

#include "exceptions.h"
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
}


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
}

TEST(PopMostSigBitTest, BitboardWithSingleSquare)
{
  U64 bb_d3 = 1ULL << d3;
  Square obs_sq_1 = popMostSigBit(bb_d3);
  Square exp_sq_1 = d3;
  EXPECT_EQ(obs_sq_1, exp_sq_1);
  EXPECT_EQ(bb_d3, 0ULL);

  U64 bb_a8 = 1ULL << a8;
  Square obs_sq_2 = popMostSigBit(bb_a8);
  Square exp_sq_2 = a8;
  EXPECT_EQ(obs_sq_1, exp_sq_1);
  EXPECT_EQ(bb_a8, 0ULL);

  U64 bb_h8 = 1ULL << h8;
  Square obs_sq_3 = popMostSigBit(bb_h8);
  Square exp_sq_3 = h8;
  EXPECT_EQ(obs_sq_3, exp_sq_3);
  EXPECT_EQ(bb_h8, 0ULL);
}

TEST(PopSigBitException, EmptyBitboardException){
  U64 empty_bb = 0ULL;
  EXPECT_THROW(popLeastSigBit(empty_bb), EmptyBitboardException);
  EXPECT_THROW(popMostSigBit(empty_bb), EmptyBitboardException);
}


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
  Test sliding attack patterns
*/
TEST(GetSlidingAttacks, SpotCheckTest)
{
  vector<vector<U64>> attacks = getSlidingAttacks();
  EXPECT_EQ(attacks[0].size(), 64);

  U64 exp_north_c5 = 0x404040000000000ULL;
  EXPECT_EQ(attacks[N][c5], exp_north_c5);

  U64 exp_north_h1 = 0x8080808080808000ULL;
  EXPECT_EQ(attacks[N][h1], exp_north_h1);

  U64 exp_north_east_c5 = 0x2010080000000000ULL;
  EXPECT_EQ(attacks[NE][c5], exp_north_east_c5);

  U64 exp_north_east_e2 = 0x8040200000ULL;
  EXPECT_EQ(attacks[NE][e2], exp_north_east_e2);

  U64 exp_east_b2 = 0xfc00ULL;
  EXPECT_EQ(attacks[E][b2], exp_east_b2);

  U64 exp_east_g7 = 1ULL << h7;
  EXPECT_EQ(attacks[E][g7], exp_east_g7);

  U64 exp_south_east_e6 = 0x2040800000ULL;
  EXPECT_EQ(attacks[SE][e6], exp_south_east_e6);

  U64 exp_south_east_a4 = 0x20408ULL;
  EXPECT_EQ(attacks[SE][a4], exp_south_east_a4);

  U64 exp_south_f2 = 0x20ULL;
  EXPECT_EQ(attacks[S][f2], exp_south_f2);

  U64 exp_south_e6 = 0x1010101010ULL;
  EXPECT_EQ(attacks[S][e6], exp_south_e6);

  U64 exp_south_west_e7 = 0x80402010000ULL;
  EXPECT_EQ(attacks[SW][e7], exp_south_west_e7);

  U64 exp_south_west_h2 = 0x40ULL;
  EXPECT_EQ(attacks[SW][h2], exp_south_west_h2);

  U64 exp_west_e5 = 0xf00000000ULL;
  EXPECT_EQ(attacks[W][e5], exp_west_e5);

  U64 exp_west_h8 = 0x7f00000000000000ULL;
  EXPECT_EQ(attacks[W][h8], exp_west_h8);

  U64 exp_north_west_d2 = 0x102040000ULL;
  EXPECT_EQ(attacks[NW][d2], exp_north_west_d2);

  U64 exp_north_west_h7 = 0x4000000000000000ULL;
  EXPECT_EQ(attacks[NW][h7], exp_north_west_h7);
}

/*
  Confirm Knight movement
*/
TEST(GetLoneKnightAttacks, CenterOfEmptyBoard)
{
  Square square = e4;
  U64 occupied = 0ULL; // unused
  U64 same_color = 1ULL << e4;
  U64 attacks = getLoneKnightAttacks(square, occupied, same_color);

  U64 exp_bb = (
    1ULL << f6 | 1ULL << g5 | 1ULL << g3 | 1ULL << f2 |
    1ULL << d2 | 1ULL << c3 | 1ULL << c5 | 1ULL << d6
  );
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneKnightAttacks, EdgeOfEmptyBoard)
{
  Square square = b8;
  U64 occupied = 0ULL; // unused
  U64 same_color = 1ULL << b8;
  U64 attacks = getLoneKnightAttacks(square, occupied, same_color);

  U64 exp_bb = 1ULL << a6 | 1ULL << c6 | 1ULL << d7;
  EXPECT_EQ(attacks, exp_bb);
}


TEST(GetLoneKnightAttacks, CantCaptureSameColor)
{
  Square square = e4;
  U64 occupied = 0ULL; // unused
  U64 same_color = 0x284410442800ULL;
  U64 attacks = getLoneKnightAttacks(square, occupied, same_color);

  U64 exp_bb = 0ULL;
  EXPECT_EQ(attacks, exp_bb);
}

/*
  Confirm Bishop movement
*/
TEST(GetLoneBishopAttacks, CenterOfEmptyBoard)
{
  Square square = e5;
  U64 occupied = 1ULL << e5;
  U64 same_color = 1ULL << e5;
  U64 attacks = getLoneBishopAttacks(square, occupied, same_color);

  U64 exp_bb = (
    1ULL << a1 | 1ULL << b2 | 1ULL << c3 | 1ULL << d4 |
    1ULL << f6 | 1ULL << g7 | 1ULL << h8 | 1ULL << b8 |
    1ULL << c7 | 1ULL << d6 | 1ULL << f4 | 1ULL << g3 | 1ULL << h2
  );
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneBishopAttacks, EdgeOfEmptyBoard)
{
  Square square = b7;
  U64 occupied = 1ULL << b7;
  U64 same_color = 1ULL << b7;
  U64 attacks = getLoneBishopAttacks(square, occupied, same_color);

  U64 exp_bb = (
    1ULL << a6 | 1ULL << c8 | 1ULL << a8 | 1ULL << c6 |
    1ULL << d5 | 1ULL << e4 | 1ULL << f3 | 1ULL << g2 | 1ULL << h1
  );
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneBishopAttacks, CompletelySurrounded)
{
  Square square = e3;
  U64 occupied = 0x28002800ULL;
  U64 same_color = 1ULL << e3;
  U64 attacks = getLoneBishopAttacks(square, occupied, same_color);

  U64 exp_bb = 1ULL << d2 | 1ULL << d4 | 1ULL << f4 | 1ULL << f2;
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneBishopAttacks, CantCaptureSameColor)
{
  Square square = e3;
  U64 occupied = 0x28002800ULL;
  U64 same_color = 0x28002800ULL;
  U64 attacks = getLoneBishopAttacks(square, occupied, same_color);

  U64 exp_bb = 0ULL;
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneBishopAttacks, LimitedMovementInCorner)
{
  Square square = g2;
  U64 occupied = 1ULL << f3;
  U64 same_color = 1ULL << g2;
  U64 attacks = getLoneBishopAttacks(square, occupied, same_color);

  U64 exp_bb = 1ULL << f1 | 1ULL << h1 | 1ULL << h3 | 1ULL << f3;
  EXPECT_EQ(attacks, exp_bb);
}

/*
  Confirm Rook movement
*/
TEST(GetLoneRookAttacks, CenterOfEmptyBoard)
{
  Square square = d4;
  U64 occupied = 1ULL << d4;
  U64 same_color = 1ULL << d4;
  U64 attacks = getLoneRookAttacks(square, occupied, same_color);

  U64 exp_bb = (
    1ULL << d1 | 1ULL << d2 | 1ULL << d3 | 1ULL << d5 |
    1ULL << d6 | 1ULL << d7 | 1ULL << d8 | 1ULL << a4 |
    1ULL << b4 | 1ULL << c4 | 1ULL << e4 | 1ULL << f4 |
    1ULL << g4 | 1ULL << h4
  );
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneRookAttacks, EdgeOfEmptyBoard)
{
  Square square = h8;
  U64 occupied = 1ULL << h8;
  U64 same_color = 1ULL << h8;
  U64 attacks = getLoneRookAttacks(square, occupied, same_color);

  U64 exp_bb = (
    1ULL << h7 | 1ULL << h6 | 1ULL << h5 | 1ULL << h4 |
    1ULL << h3 | 1ULL << h2 | 1ULL << h1 | 1ULL << a8 |
    1ULL << b8 | 1ULL << c8 | 1ULL << d8 | 1ULL << e8 |
    1ULL << f8 | 1ULL << g8
  );
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneRookAttacks, CompletelySurrounded)
{
  Square square = d4;
  U64 occupied = 0x814080000ULL;
  U64 same_color = 1ULL << d4;
  U64 attacks = getLoneRookAttacks(square, occupied, same_color);

  U64 exp_bb = 1ULL << d5 | 1ULL << e4 | 1ULL << d3 | 1ULL << c4;
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneRookAttacks, CantCaptureSameColor)
{
  Square square = d4;
  U64 occupied = 0x814080000ULL;
  U64 same_color = 0x814080000ULL;
  U64 attacks = getLoneRookAttacks(square, occupied, same_color);

  U64 exp_bb = 0ULL;
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneRookAttacks, LimitedMovementInCorner)
{
  Square square = g7;
  U64 occupied = 0x20400000000000ULL;
  U64 same_color = 1ULL << g7;
  U64 attacks = getLoneRookAttacks(square, occupied, same_color);

  U64 exp_bb = 1ULL << g8 | 1ULL << h7 | 1ULL << f7 | 1ULL << g6;
  EXPECT_EQ(attacks, exp_bb);
}

/*
  Confirm Queen movement
*/
TEST(GetLoneQueenAttacks, CenterOfEmptyBoard)
{
  Square square = d5;
  U64 occupied = 1ULL << d5;
  U64 same_color = 1ULL << d5;
  U64 attacks = getLoneQueenAttacks(square, occupied, same_color);
  
  U64 exp_bb = (
    1ULL << d1 | 1ULL << d2 | 1ULL << d3 | 1ULL << d4 | 1ULL << d6 |
    1ULL << d7 | 1ULL << d8 | 1ULL << a5 | 1ULL << b5 | 1ULL << c5 |
    1ULL << e5 | 1ULL << f5 | 1ULL << g5 | 1ULL << h5 | 1ULL << a2 |
    1ULL << b3 | 1ULL << c4 | 1ULL << e6 | 1ULL << f7 | 1ULL << g8 |
    1ULL << a8 | 1ULL << b7 | 1ULL << c6 | 1ULL << e4 | 1ULL << f3 |
    1ULL << g2 | 1ULL << h1
  );
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneQueenAttacks, EdgeOfEmptyBoard)
{
  Square square = g2;
  U64 occupied = 1ULL << g2;
  U64 same_color = 1ULL << g2;
  U64 attacks = getLoneQueenAttacks(square, occupied, same_color);

  U64 exp_bb = (
    1ULL << a2 | 1ULL << b2 | 1ULL << c2 | 1ULL << d2 | 1ULL << e2 |
    1ULL << f2 | 1ULL << h2 | 1ULL << g1 | 1ULL << g3 | 1ULL << g4 |
    1ULL << g5 | 1ULL << g6 | 1ULL << g7 | 1ULL << g8 | 1ULL << a8 |
    1ULL << b7 | 1ULL << c6 | 1ULL << d5 | 1ULL << e4 | 1ULL << f3 |
    1ULL << h1 | 1ULL << f1 | 1ULL << h3
  );
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneQueenAttacks, CompletelySurrounded)
{
  Square square = c4;
  U64 occupied = 0xe0a0e0000ULL;
  U64 same_color = 1ULL << c4;
  U64 attacks = getLoneQueenAttacks(square, occupied, same_color);

  U64 exp_bb = (
    1ULL << c5 | 1ULL << d5 | 1ULL << d4 | 1ULL << d3 |
    1ULL << c3 | 1ULL << b3 | 1ULL << b4 | 1ULL << b5
  );
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneQueenAttacks, CantCaptureSameColor)
{
  Square square = c4;
  U64 occupied = 0xe0a0e0000ULL;
  U64 same_color = 0xe0a0e0000ULL;
  U64 attacks = getLoneQueenAttacks(square, occupied, same_color);

  U64 exp_bb = 0ULL;
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneQueenAttacks, LimitedMovementInCorner)
{
  Square square = b7;
  U64 occupied = 0x404070000000000ULL;
  U64 same_color = 1ULL << b7;
  U64 attacks = getLoneQueenAttacks(square, occupied, same_color);

  U64 exp_bb = (
    1ULL << a8 | 1ULL << a7 | 1ULL << b8 | 1ULL << a6 |
    1ULL << c8 | 1ULL << b6 | 1ULL << c6 | 1ULL << c7
  );
  EXPECT_EQ(attacks, exp_bb);
}


/*
  Confirm King movement
*/
TEST(GetLoneKingAttacksTest, CenterOfBoard)
{
  Square square = d4;
  U64 occupied = 0ULL;
  U64 same_color = 1ULL << d4;
  U64 attacks = getLoneKingAttacks(square, occupied, same_color);

  U64 exp_bb = (
    1ULL << c4 | 1ULL << c5 | 1ULL << d5 | 1ULL << e5 |
    1ULL << e4 | 1ULL << e3 | 1ULL << d3 | 1ULL << c3
  );
  EXPECT_EQ(attacks, exp_bb);
}

TEST(GetLoneKingAttacksTest, SideOfBoard)
{
  Square square = h5;
  U64 occupied = 0ULL;
  U64 same_color = 1ULL << h5;
  U64 attacks = getLoneKingAttacks(square, occupied, same_color);

  U64 exp_bb = 1ULL << h6 | 1ULL << g6 | 1ULL << g5 | 1ULL << g4 | 1ULL << h4;
  EXPECT_EQ(attacks, exp_bb);
}

#ifndef _PIECE_H_
#define _PIECE_H_

#include <vector>

#include "square.h"
#include "types.h"


Square popLeastSigBit(U64 &piece_bb);
Square popMostSigBit (U64 &piece_bb);
Square getLeastSigBit(U64 piece_bb);
Square getMostSigBit (U64 piece_bb);

/* 
  Single square movements
*/

U64 northOne    (U64 &piece_bb);
U64 southOne    (U64 &piece_bb);
U64 eastOne     (U64 &piece_bb);
U64 westOne     (U64 &piece_bb);
U64 northEastOne(U64 &piece_bb);
U64 southEastOne(U64 &piece_bb);
U64 southWestOne(U64 &piece_bb);
U64 northWestOne(U64 &piece_bb);


/*
  Knight movements
*/

U64 knightNorthNorthEast(U64 &bb);
U64 knightNorthEastEast (U64 &bb);
U64 knightSouthEastEast (U64 &bb);
U64 knightSouthSouthEast(U64 &bb);
U64 knightSouthSouthWest(U64 &bb);
U64 knightSouthWestWest (U64 &bb);
U64 knightNorthWestWest (U64 &bb);
U64 knightNorthNorthWest(U64 &bb);


/*
  Sliding piece movements
*/

std::vector<std::vector<U64>> getSlidingAttacks();

U64 getDiagAttacks(Square square, U64 &occupied);
U64 getVertHorizAttacks(Square square, U64 &occupied);

/*
  Attack map generation
*/
U64 getLonePawnAttacks(Square square, U64 &occupied, U64 &same_color,
                       Color color, bool &promotion, Square en_passant = nullsq,
                       bool attack_empty_squares = false);
U64 getLoneKnightAttacks(Square square, U64 &occupied, U64 &same_color);
U64 getLoneBishopAttacks(Square square, U64 &occupied, U64 &same_color);
U64 getLoneRookAttacks  (Square square, U64 &occupied, U64 &same_color);
U64 getLoneQueenAttacks (Square square, U64 &occupied, U64 &same_color);
U64 getLoneKingAttacks  (Square square, U64 &occupied, U64 &same_color);

U64 getPawnAttacks(U64 pawn_bb, U64 &occupied, U64 &same_color,
                   Color color, bool &promotion, bool attack_empty_squares);
U64 getPieceAttacks(PieceType piece_type, U64 piece_bb, U64 &occupied,
                    U64 &same_color);

#endif  // _PIECE_H_


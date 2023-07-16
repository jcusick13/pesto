#include <bit>

#include "piece.h"


/*
  Find the least significant non-zero bit. Flip it
  and return the `Square` it represents.
*/
Square popLeastSigBit(U64 &piece_bb)
{
  int first_non_zero_idx = std::countr_zero(piece_bb);
  piece_bb &= ~(1ULL << first_non_zero_idx);

  return Square(first_non_zero_idx);
};


/*
  Single square movements
*/

U64 northOne    (U64 &piece_bb){ return piece_bb << 8; }
U64 southOne    (U64 &piece_bb){ return piece_bb >> 8; }
U64 eastOne     (U64 &piece_bb){ return piece_bb << 1 & ~FileA; }
U64 westOne     (U64 &piece_bb){ return piece_bb >> 1 & ~FileH; }
U64 northEastOne(U64 &piece_bb){ return piece_bb << 9 & ~FileA; }
U64 southEastOne(U64 &piece_bb){ return piece_bb >> 7 & ~FileA; }
U64 southWestOne(U64 &piece_bb){ return piece_bb >> 9 & ~FileH; }
U64 northWestOne(U64 &piece_bb){ return piece_bb << 7 & ~FileH; }

/*
  Knight movements
*/
U64 knightNorthNorthEast(U64 &bb){ return bb << 17 & ~FileA; }
U64 knightNorthEastEast (U64 &bb){ return bb << 10 & ~FileA & ~FileB; }
U64 knightSouthEastEast (U64 &bb){ return bb >> 6  & ~FileA & ~FileB; }
U64 knightSouthSouthEast(U64 &bb){ return bb >> 15 & ~FileA; }
U64 knightSouthSouthWest(U64 &bb){ return bb >> 17 & ~FileH; }
U64 knightSouthWestWest (U64 &bb){ return bb >> 10 & ~FileG & ~FileH; }
U64 knightNorthWestWest (U64 &bb){ return bb << 6  & ~FileG & ~FileH; }
U64 knightNorthNorthWest(U64 &bb){ return bb << 15 & ~FileH; }


/*
  Attack map generation
*/


/*
  Return bitboard with squares attacked by a knight
*/
U64 getKnightAttacks(U64 &knight_bb)
{
  U64 no_no_ea = knightNorthNorthEast(knight_bb);
  U64 no_ea_ea = knightNorthEastEast (knight_bb);
  U64 so_ea_ea = knightSouthEastEast (knight_bb);
  U64 so_so_ea = knightSouthSouthEast(knight_bb);
  U64 so_so_we = knightSouthSouthWest(knight_bb);
  U64 so_we_we = knightSouthWestWest (knight_bb);
  U64 no_we_we = knightNorthWestWest (knight_bb);
  U64 no_no_we = knightNorthNorthWest(knight_bb);

  return (
    no_no_ea | no_ea_ea | so_ea_ea | so_so_ea |
    so_so_we | so_we_we | no_we_we | no_no_we
  );
}

/*
  Return bitboard with sqaures attacked by a king
*/
U64 getKingAttacks(U64 &king_bb)
{
  // TODO: Assert only one king
  U64 north = northOne(king_bb);
  U64 south = southOne(king_bb);
  U64 east  = eastOne (king_bb);
  U64 west  = westOne (king_bb);

  U64 north_east = northEastOne(king_bb);
  U64 south_east = southEastOne(king_bb);
  U64 south_west = southWestOne(king_bb);
  U64 north_west = northWestOne(king_bb);

  return (
    north | south | east | west |
    north_east | south_east | south_west | north_west
  );
}

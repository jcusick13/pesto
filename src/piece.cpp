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

U64 northOne(U64 &piece_bb)    { return piece_bb << 8; }
U64 southOne(U64 &piece_bb)    { return piece_bb >> 8; }
U64 eastOne (U64 &piece_bb)    { return piece_bb << 1 & ~FileA; }
U64 westOne (U64 &piece_bb)    { return piece_bb >> 1 & ~FileH; }
U64 northEastOne(U64 &piece_bb){ return piece_bb << 9 & ~FileA & ~Rank1; }
U64 southEastOne(U64 &piece_bb){ return piece_bb >> 7 & ~FileA & ~Rank8; }
U64 southWestOne(U64 &piece_bb){ return piece_bb >> 9 & ~FileH & ~Rank8; }
U64 northWestOne(U64 &piece_bb){ return piece_bb << 7 & ~FileH & ~Rank1; }

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

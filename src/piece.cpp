#include <algorithm>
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
  Sliding piece movements
*/


/*
  Computes and returns a length-4 vector of attack
  bitboards for NORTH, SOUTH, EAST, WEST, where each
  individual vector is arranged with squares a1..h8
  in cells 0..63.

  Builds north and east attacks from a1, moving
  across files then up ranks. South and west attacks
  start from h8, moving across files, then down ranks.

  The south and west vectors are then reveresed
  before being returned such that each directional
  vector has a 0..63 square ordering.
*/
vector<vector<U64>> getSlidingAttacks()
{
  vector<U64> FileVec = {
    FileA, FileB, FileC, FileD,
    FileE, FileF, FileG, FileH,
  };

  vector<U64> north, south, east, west;
  U64 north_attack = 0x101010101010100ULL;
  U64 south_attack = 0x80808080808080ULL;
  U64 east_attack = 0xfeULL;
  U64 west_attack = 0x7f00000000000000ULL;

  for (int rank = 0; rank < 8; rank++){
    for (int file = 0; file < 8; file++){

      north.push_back(north_attack << file);
      south.push_back(south_attack >> file);

      // Manually create 'exclude' bitboards for east/west
      // attacks, as shifting bits across files can wrap
      // bits around the board (north/south bitshifting
      // instead just drops the bit at the end of the board)
      U64 east_exclude_files = FileA;
      U64 west_exclude_files = FileH;
      for (int i = 0; i < file; i++){
        east_exclude_files |= FileVec[i];
        west_exclude_files |= FileVec[7 - i];
      }
      east.push_back((east_attack << file) & ~east_exclude_files);
      west.push_back((west_attack >> file) & ~west_exclude_files);

    }
    north_attack = north_attack << 8;
    south_attack = south_attack >> 8;
    east_attack = east_attack << 8;
    west_attack = west_attack >> 8;
  }

  std::reverse(south.begin(), south.end());
  std::reverse(west.begin(), west.end());

  return vector<vector<U64>> {north, south, east, west};
}


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

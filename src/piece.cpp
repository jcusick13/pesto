#include <algorithm>
#include <bit>

#include "exceptions.h"
#include "piece.h"


/*
  Find the least significant non-zero bit. Flip it
  and return the `Square` it represents.
*/
Square popLeastSigBit(U64 &piece_bb)
{
  int first_non_zero_idx = std::countr_zero(piece_bb);
  if (first_non_zero_idx == 64) {
    throw EmptyBitboardException();
  }

  piece_bb &= ~(1ULL << first_non_zero_idx);
  return Square(first_non_zero_idx);
};

/*
  Find the most significant non-zero bit. Flip it
  and return the `Square` it represents.
*/
Square popMostSigBit(U64 &piece_bb)
{
  int last_non_zero_idx = 63 - std::countl_zero(piece_bb);
  if (last_non_zero_idx < 0) {
    throw EmptyBitboardException();
  }

  piece_bb &= ~(1ULL << last_non_zero_idx);
  return Square(last_non_zero_idx);
}


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
  Computes and returns a length-8 vector of attack
  bitboards for NORTH, SOUTH, EAST, ...,  where each
  individual vector is arranged with squares a1..h8
  in cells 0..63.

  Builds north and east attacks from a1, moving
  across files then up ranks. South and west attacks
  start from h8, moving across files, then down ranks.

  The south and west vectors are then reveresed
  before being returned such that each directional
  vector has a 0..63 square ordering.
*/
std::vector<std::vector<U64>> getSlidingAttacks()
{
  std::vector<U64> FileVec = {
    FileA, FileB, FileC, FileD,
    FileE, FileF, FileG, FileH,
  };

  std::vector<U64> north, south, east, west;
  std::vector<U64> neast, nwest, seast, swest;
  U64 north_attack = 0x101010101010100ULL;
  U64 south_attack = 0x80808080808080ULL;
  U64 east_attack = 0xfeULL;
  U64 west_attack = 0x7f00000000000000ULL;
  U64 neast_attack = 0x8040201008040200ULL;
  U64 nwest_attack = 0x102040810204000ULL;
  U64 seast_attack = 0x2040810204080ULL;
  U64 swest_attack = 0x40201008040201ULL;

  for (int rank = 0; rank < 8; rank++){

    // Each row of 8 entries for northwest, southeast need
    // to be reversed before added in correct order to the
    // full length-64 vector
    std::vector<U64> nwest_tmp;
    std::vector<U64> seast_tmp;

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
      neast.push_back((neast_attack << file) & ~east_exclude_files);
      nwest_tmp.push_back((nwest_attack >> file) & ~west_exclude_files);
      seast_tmp.push_back((seast_attack << file) & ~east_exclude_files);
      swest.push_back((swest_attack >> file) & ~west_exclude_files);
    }

    north_attack = north_attack << 8;
    south_attack = south_attack >> 8;
    east_attack = east_attack << 8;
    west_attack = west_attack >> 8;

    neast_attack = neast_attack << 8;
    nwest_attack = nwest_attack << 8;
    seast_attack = seast_attack >> 8;
    swest_attack = swest_attack >> 8;

    // Northwest & southeast attacks are calculated from h_n to a_n
    // and need to be flipped at the end of each rank's processing
    std::reverse(nwest_tmp.begin(), nwest_tmp.end());
    nwest.insert(nwest.end(), nwest_tmp.begin(), nwest_tmp.end());

    std::reverse(seast_tmp.begin(), seast_tmp.end());
    seast.insert(seast.end(), seast_tmp.begin(), seast_tmp.end());
  }

  std::reverse(south.begin(), south.end());
  std::reverse(west.begin(), west.end());
  std::reverse(swest.begin(), swest.end());
  std::reverse(seast.begin(), seast.end());

  return std::vector<std::vector<U64>> {
    north, neast, east, seast, south, swest, west, nwest
  };
}

std::vector<std::vector<U64>> SLIDING_ATTACKS = getSlidingAttacks();

/*
  Generate an attack bitboard based on diagnoal
  rays, starting from `square` and recognizing
  squares that are occupied
*/
U64 getDiagAttacks(Square square, U64 &occupied)
{
  U64 northeast = SLIDING_ATTACKS[NE][square];
  U64 northeast_blockers = northeast & occupied;
  if (northeast_blockers){
    Square ne_first_blocker = popLeastSigBit(northeast_blockers);
    northeast &= ~SLIDING_ATTACKS[NE][ne_first_blocker];
  }

  U64 southeast = SLIDING_ATTACKS[SE][square];
  U64 southeast_blockers = southeast & occupied;
  if (southeast_blockers){
    Square se_first_blocker = popMostSigBit(southeast_blockers);
    southeast &= ~SLIDING_ATTACKS[SE][se_first_blocker];
  }

  U64 southwest = SLIDING_ATTACKS[SW][square];
  U64 southwest_blockers = southwest & occupied;
  if (southwest_blockers){
    Square sw_first_blocker = popMostSigBit(southwest_blockers);
    southwest &= ~SLIDING_ATTACKS[SW][sw_first_blocker];
  }

  U64 northwest = SLIDING_ATTACKS[NW][square];
  U64 northwest_blockers = northwest & occupied;
  if (northwest_blockers){
    Square nw_first_blocker = popLeastSigBit(northwest_blockers);
    northwest &= ~SLIDING_ATTACKS[NW][nw_first_blocker];
  }

  return northeast | southeast | southwest | northwest;
}

/*
  Generate an attack bitboard based on vertical
  and horizontal rays, starting from `square`
  and recognizing squares that are occupied
*/
U64 getVertHorizAttacks(Square square, U64 &occupied)
{
  U64 north = SLIDING_ATTACKS[N][square];
  U64 north_blockers = north & occupied;
  if (north_blockers){
    Square n_first_blocker = popLeastSigBit(north_blockers);
    north &= ~SLIDING_ATTACKS[N][n_first_blocker];
  }
  
  U64 east = SLIDING_ATTACKS[E][square];
  U64 east_blockers = east & occupied;
  if (east_blockers){
    Square e_first_blocker = popLeastSigBit(east_blockers);
    east &= ~SLIDING_ATTACKS[E][e_first_blocker];
  }

  U64 south = SLIDING_ATTACKS[S][square];
  U64 south_blockers = south & occupied;
  if (south_blockers){
    Square s_first_blocker = popMostSigBit(south_blockers);
    south &= ~SLIDING_ATTACKS[S][s_first_blocker];
  }

  U64 west = SLIDING_ATTACKS[W][square];
  U64 west_blockers = west & occupied;
  if (west_blockers){
    Square w_first_blocker = popMostSigBit(west_blockers);
    west &= ~SLIDING_ATTACKS[W][w_first_blocker];
  }

  return north | east | south | west;
}


/*
  Attack map generation
*/

U64 getLonePawnAttacks(Square square, U64 &occupied, U64 &same_color,
                       Color color, bool &promotion, Square en_passant){
    
    U64 pawn_bb = 1ULL << square;

    U64 move_one_forward;
    if (color == WHITE) {
      move_one_forward = (pawn_bb << 8) & ~occupied;
    } else {
      move_one_forward = (pawn_bb >> 8) & ~occupied;
    }

    U64 move_two_forward = 0ULL;
    if (move_one_forward) {
      // If pawn is unable to move one square forward,
      // it's not possible for it to move two forward
      if ((color == WHITE) && (pawn_bb & Rank2)){
        move_two_forward = (pawn_bb << 16) & ~occupied;
      }
      if ((color == BLACK) && (pawn_bb & Rank7)) {
        move_two_forward = (pawn_bb >> 16) & ~occupied;
      }
    }

    U64 capture_diag;
    U64 capture_en_passant;
    if (color == WHITE) {
      capture_diag = pawn_bb << 7 | pawn_bb << 9;
      capture_en_passant = pawn_bb << 7 | pawn_bb << 9;
    } else {
      capture_diag = pawn_bb >> 7 | pawn_bb >> 9;
      capture_en_passant = pawn_bb >> 7 | pawn_bb >> 9;
    }
    if (!(capture_diag && occupied)) {
       capture_diag = 0ULL; 
    } else {
      capture_diag &= occupied;
    }
    capture_en_passant &= (1ULL << en_passant);


    U64 attacks = (
      move_one_forward | move_two_forward | capture_diag | capture_en_passant
    ) & ~same_color;

    promotion = false;
    if (
      ((color == WHITE) && (attacks & Rank8)) |
      ((color == BLACK) && (attacks & Rank1))
    ) {
      promotion = true;
    }
    
    return attacks;
}

U64 getLoneKnightAttacks(Square square, U64 &occupied, U64 &same_color)
{
  U64 knight_bb = 1ULL << square;
  U64 no_no_ea = knightNorthNorthEast(knight_bb);
  U64 no_ea_ea = knightNorthEastEast (knight_bb);
  U64 so_ea_ea = knightSouthEastEast (knight_bb);
  U64 so_so_ea = knightSouthSouthEast(knight_bb);
  U64 so_so_we = knightSouthSouthWest(knight_bb);
  U64 so_we_we = knightSouthWestWest (knight_bb);
  U64 no_we_we = knightNorthWestWest (knight_bb);
  U64 no_no_we = knightNorthNorthWest(knight_bb);

  U64 attacks = (
    no_no_ea | no_ea_ea | so_ea_ea | so_so_ea |
    so_so_we | so_we_we | no_we_we | no_no_we
  );
  return attacks & ~same_color;
}

U64 getLoneBishopAttacks(Square square, U64 &occupied, U64 &same_color)
{
  U64 attacks = getDiagAttacks(square, occupied);
  return attacks & ~same_color;
}


U64 getLoneRookAttacks(Square square, U64 &occupied, U64 &same_color)
{
  U64 attacks = getVertHorizAttacks(square, occupied);
  return attacks & ~same_color;
}

U64 getLoneQueenAttacks(Square square, U64 &occupied, U64 &same_color)
{
  U64 attack_diag = getDiagAttacks(square, occupied);
  U64 attack_vert_horiz = getVertHorizAttacks(square, occupied);
  return (attack_diag | attack_vert_horiz) & ~same_color;
}

U64 getLoneKingAttacks(Square square, U64 &occupied, U64 &same_color)
{
  U64 king_bb = 1ULL << square;
  U64 north = northOne(king_bb);
  U64 south = southOne(king_bb);
  U64 east  = eastOne (king_bb);
  U64 west  = westOne (king_bb);

  U64 north_east = northEastOne(king_bb);
  U64 south_east = southEastOne(king_bb);
  U64 south_west = southWestOne(king_bb);
  U64 north_west = northWestOne(king_bb);

  U64 attacks = (
    north | south | east | west |
    north_east | south_east | south_west | north_west
  );
  return attacks & ~same_color;
}


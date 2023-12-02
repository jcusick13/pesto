#include <functional>
#include <vector>

#include "exceptions.h"
#include "move.h"
#include "piece.h"


void addPieceTypeMoves(PieceType &piece_type, std::vector<Move> *moves,
                       U64 pieces, U64 &occupied, U64 &same_color) {

  std::function<U64(Square, U64 &, U64 &)> getPieceAttacks;
  switch(piece_type) {
    case KNIGHT:
      getPieceAttacks = getLoneKnightAttacks;
      break;
    
    case BISHOP:
      getPieceAttacks = getLoneBishopAttacks;
      break;

    case ROOK:
      getPieceAttacks = getLoneRookAttacks;
      break;
    
    case QUEEN:
      getPieceAttacks = getLoneQueenAttacks;
    
    case KING:
      getPieceAttacks = getLoneKingAttacks;
  }

  while (true) {
    try {
      Square from_sq = popLeastSigBit(pieces);
      U64 attacks = getPieceAttacks(from_sq, occupied, same_color);

      while (true) {
        try {
          Square to_sq = popLeastSigBit(attacks);
          Move move(from_sq, to_sq);
          moves->push_back(move);
        } catch(EmptyBitboardException){ break; }
      }
    } catch(EmptyBitboardException){ break; }
  }
}

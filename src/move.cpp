#include <functional>
#include <vector>

#include "exceptions.h"
#include "move.h"
#include "piece.h"
#include "types.h"


std::vector<PieceType> promotionPieces {KNIGHT, BISHOP, ROOK, QUEEN};


void addPawnMoves(std::vector<Move> *moves, U64 pawns, U64 &occupied,
                  Color color, U64 &same_color, Square en_passant) {

  while (true) {
    try {
      Square from_sq = popLeastSigBit(pawns);
      bool promotion = false;
      U64 attacks = getLonePawnAttacks(from_sq, occupied, same_color, color,
                                       promotion, en_passant);
      while (true) {
        try {
          Square to_sq = popLeastSigBit(attacks);

          if (promotion) {
            for (PieceType piece : promotionPieces) {
              Move move(from_sq, to_sq, piece);
              moves->push_back(move);
            }
          } else {
            Move move(from_sq, to_sq);
            moves->push_back(move);
          }

        } catch(EmptyBitboardException){ break; }
      }
    } catch(EmptyBitboardException){ break; }
  }
}


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
      break;
    
    case KING:
      getPieceAttacks = getLoneKingAttacks;
      break;
    
    default:
      throw InvalidPieceException();
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


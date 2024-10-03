#include <functional>
#include <iostream>
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

          PieceType captured = NULL_PIECE;
          Square ep_capture = nullsq;
          if (to_sq == en_passant) {
            captured = PAWN;
            if (color == WHITE) { ep_capture = Square(to_sq - 8); }
            else { ep_capture = Square(to_sq + 8); }
          }

          if (promotion) {
            for (PieceType piece : promotionPieces) {
              Move move(from_sq, to_sq, piece, captured, ep_capture);
              moves->push_back(move);
            }
          } else {
            Move move(from_sq, to_sq, NULL_PIECE, captured, ep_capture);
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


void applyMove(Pieces *pieces, Move &move, Color to_move) {
  U64 from_bb = 1ULL << move.from;
  U64 to_bb = 1ULL << move.to;
  Color other{to_move ^ BLACK};

  // Find the bitboard with the piece to be moved
  bool found_piece_to_move = false;
  PieceType from_piece_type;
  bb_vec *from_piece_bb;
  for (int ptype = PAWN; ptype != NULL_PIECE; ++ptype) {
    from_piece_type = PieceType(ptype);
    from_piece_bb = pieces->get(from_piece_type);
    if ((from_piece_bb->at(to_move) & from_bb) != 0) {
      found_piece_to_move = true;
      break;
    }
  }
  if (!found_piece_to_move) { throw InvalidPieceException(); }

  // Zero out bit for the starting Square
  from_piece_bb->at(to_move) &= ~(from_bb);

  // Check if a capture occurred
  bool captured_piece = false;
  PieceType opp_piece_type;
  bb_vec *opp_piece_bb;
  for (int ptype = PAWN; ptype != NULL_PIECE; ++ptype) {
    opp_piece_type = PieceType(ptype);
    opp_piece_bb = pieces->get(opp_piece_type);
    if ((opp_piece_bb->at(other) & to_bb) != 0) {
      captured_piece = true;
      break;
    }
  }

  if (captured_piece) {
    opp_piece_bb->at(other) &= ~(to_bb);
    move.captured = opp_piece_type;
  }

  if (move.ep_capture != nullsq) {
    pieces->get(PAWN)->at(other) &= ~(1ULL << move.ep_capture);
  }

  // Flip bit of bitboard for the ending square
  if (move.promotion != NULL_PIECE) {
    pieces->get(move.promotion)->at(to_move) |= to_bb;
  } else {
    from_piece_bb->at(to_move) |= to_bb;
  }
}

void revertMove(Pieces *pieces, Move &move, Color moved) {
  // From reference of how the original move was made
  U64 from_bb = 1ULL << move.from;
  U64 to_bb = 1ULL << move.to;
  Color other{moved ^ BLACK};

  // Find the bitboard with the piece to be reverted
  bool found_piece_to_revert = false;
  PieceType moved_piece_type;
  bb_vec *moved_piece_bb;
  for (int ptype = PAWN; ptype != NULL_PIECE; ++ptype) {
    moved_piece_type = PieceType(ptype);
    moved_piece_bb = pieces->get(moved_piece_type);
    if ((moved_piece_bb->at(moved) & to_bb) != 0) {
      found_piece_to_revert = true;
      break;
    }
  }
  if (!found_piece_to_revert) { throw InvalidPieceException(); }

  // Zero out bit for the ending square
  moved_piece_bb->at(moved) &= ~(to_bb);

  // Reset captured piece
  if (move.captured != NULL_PIECE) {
    if (move.ep_capture != nullsq) {
      pieces->get(PAWN)->at(other) |= (1ULL << move.ep_capture);
    } else {
      pieces->get(move.captured)->at(other) |= to_bb;
    }
  }

  // Add piece back to it's original square
  if (move.promotion != NULL_PIECE) {
    pieces->get(PAWN)->at(moved) |= from_bb;
  } else {
    moved_piece_bb->at(moved) |= from_bb;
  }
}


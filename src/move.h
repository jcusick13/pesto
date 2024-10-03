#ifndef _MOVE_H_
#define _MOVE_H_

#include <vector>

#include "collections.h"
#include "square.h"
#include "types.h"


struct Move{
  Square from;
  Square to;
  PieceType promotion;
  PieceType captured;
  // Location of the piece that was _captured_,
  // not where the capturing piece moved to
  Square ep_capture;

  Move(Square from, Square to) : from(from), to(to) { 
    promotion = NULL_PIECE;
    captured = NULL_PIECE;
    ep_capture = nullsq;
  };

  Move(Square from, Square to, PieceType promotion) : from(from), to(to),
    promotion(promotion) {
      captured = NULL_PIECE;
      ep_capture = nullsq;
  };

  Move(Square from, Square to, PieceType promotion, PieceType captured)
    : from(from), to(to), promotion(promotion), captured(captured) {
      ep_capture = nullsq;
  };

  Move(Square from, Square to, PieceType promotion, PieceType captured,
       Square ep_capture) :
    from(from), to(to), promotion(promotion), captured(captured),
    ep_capture(ep_capture) {};

  bool operator==(const Move &other) const {
      return (
        from == other.from
        && to == other.to
        && promotion == other.promotion
        && captured == other.captured
        && ep_capture == other.ep_capture
      );
  }
};


void addPawnMoves(std::vector<Move> *moves, U64 pawns, U64 &occupied,
                  Color color, U64 &same_color, Square en_passant);
void addPieceTypeMoves(PieceType &piece_type, std::vector<Move> *moves, 
                       U64 pieces, U64 &occupied, U64 &same_color);

void applyMove(Pieces *pieces, Move &move, Color to_move);
void revertMove(Pieces *pieces, Move &move, Color moved);

#endif  // _MOVE_H_


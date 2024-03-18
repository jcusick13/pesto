#ifndef _BOARD_H_
#define _BOARD_H_

#include <string>
#include "collections.h"
#include "square.h"
#include "types.h"


class Board {
  public:
    Board();

    void fromFen(std::string fen);
    std::string toFen();
    
    Pieces pieces;
    Color to_move;
    int ply;
    int halfmove_clock;
    Square en_passant_target;
    CastleRights castle_white;
    CastleRights castle_black;
};

#endif  // _BOARD_H_
  

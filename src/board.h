#ifndef _BOARD_H_
#define _BOARD_H_

#include <vector>
#include "types.h"


class Board {
  public:
    Board();

    std::vector<U64> pawns   = std::vector<U64>(2);
    std::vector<U64> knights = std::vector<U64>(2);
    std::vector<U64> bishops = std::vector<U64>(2);
    std::vector<U64> rooks   = std::vector<U64>(2);
    std::vector<U64> queens  = std::vector<U64>(2);
    std::vector<U64> kings   = std::vector<U64>(2);
};

#endif  // _BOARD_H_


#ifndef _COLLECTIONS_H_
#define _COLLECTIONS_H_

#include <vector>
#include "types.h"

class CastleRights {
  public:
    CastleRights();
    CastleRights(bool kingside, bool queenside);

    bool operator==(const CastleRights &other) const;

    bool kingside;
    bool queenside;
};

class Pieces {
  public:
    Pieces();

    void initStartingPosition();

    std::vector<U64> pawns; 
    std::vector<U64> knights;
    std::vector<U64> bishops;
    std::vector<U64> rooks;
    std::vector<U64> queens;
    std::vector<U64> kings;
};

#endif  // _COLLECTIONS_H_


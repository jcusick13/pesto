#ifndef _COLLECTIONS_H_
#define _COLLECTIONS_H_

#include <memory>
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

    std::vector<U64>* get(PieceType piece_type);
    U64 getColor(Color color);
    U64 occupied();

  private:
    std::unique_ptr<std::vector<U64>> _pawns;
    std::unique_ptr<std::vector<U64>> _knights;
    std::unique_ptr<std::vector<U64>> _bishops;
    std::unique_ptr<std::vector<U64>> _rooks;
    std::unique_ptr<std::vector<U64>> _queens;
    std::unique_ptr<std::vector<U64>> _kings;
};

#endif  // _COLLECTIONS_H_


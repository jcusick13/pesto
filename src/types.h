#ifndef _TYPES_H_
#define _TYPES_H_

#include <cstdint>

typedef uint64_t U64;

enum Color: int {
  WHITE, BLACK
};

enum Direction: int {
  N, NE, E, SE, S, SW, W, NW
};

enum PieceType: int {
  PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
};

constexpr U64 FileA = 0x0101010101010101ULL;
constexpr U64 FileB = FileA << 1;
constexpr U64 FileC = FileA << 2;
constexpr U64 FileD = FileA << 3;
constexpr U64 FileE = FileA << 4;
constexpr U64 FileF = FileA << 5;
constexpr U64 FileG = FileA << 6;
constexpr U64 FileH = FileA << 7;

#endif  // _MOVE_H_

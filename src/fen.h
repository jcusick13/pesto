#ifndef _FEN_H_
#define _FEN_H_

#include <string>
#include <tuple>
#include <vector>
#include "collections.h"
#include "square.h"

std::vector<std::string> splitString(std::string s, std::string delimiter);
bool isDigit(const std::string s);

std::string dumpCastlingRightsToFen(CastleRights white, CastleRights black);
std::string dumpEnPassantTargetToFen(Square square);
std::string dumpPiecesToFen(Pieces pieces);

std::tuple<CastleRights, CastleRights> parseFenCastlingRights(std::string fen);
Square parseFenEnPassantTarget(std::string fen);
Pieces parseFenPieces(std::string fen);


#endif  // _FEN_H_


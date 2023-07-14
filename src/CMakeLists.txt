add_library(
    board 
    board.cpp
)
target_include_directories(
    board PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_library(
    piece 
    piece.cpp
)
target_include_directories(
    piece PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

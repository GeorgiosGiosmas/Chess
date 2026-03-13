"""
conftest.py - Shared fixtures and helpers for all chess engine tests.
"""

import sys
import os
import pytest

# Add the project root to the path so we can import piece and board
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from board import Board
from piece import King, Queen, Rook, Bishop, Knight, Pawn


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def board_with_pieces():
    """
    Fresh board with all pieces initialized and moves computed.
    Equivalent to the start of a new game.
    """
    board = Board()
    board.board_initialize_pieces()
    history = []
    board.get_all_pieces_moves(history)
    board.filter_legal_moves(history)
    return board, history


@pytest.fixture
def empty_board():
    """
    Empty board for custom piece placement.
    No pieces are placed - use place_piece() to set up positions.
    """
    board = Board()
    history = []
    return board, history


# ============================================================
# Helper Functions (not fixtures - used directly in tests)
# ============================================================

def place_piece(board, piece, square_str):
    """Place a piece on the board by algebraic notation (e.g. 'e4')."""
    sq = board.board_get_square(square_str)
    sq.piece_on_square = piece
    if isinstance(piece, King):
        if piece.colour == 'w':
            board.white_king_square = sq
        else:
            board.black_king_square = sq


def make_move(board, from_sq, to_sq, history):
    """
    Execute a move and recompute all legal moves afterwards.
    Returns 0 on success, -1 if the move was invalid.
    """
    result = board.make_move(from_sq, to_sq, history)
    if result == 0:
        board.get_all_pieces_moves(history)
        board.filter_legal_moves(history)
    return result


def compute_moves(board, history):
    """Compute and filter legal moves for the current position."""
    board.get_all_pieces_moves(history)
    board.filter_legal_moves(history)

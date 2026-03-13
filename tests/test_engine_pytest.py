"""
test_engine_pytest.py - 150 pytest tests for the chess engine.

Run all tests:              pytest tests/test_engine_pytest.py -v
Run a single section:       pytest tests/test_engine_pytest.py -v -k "Openings"
Run by marker:              pytest tests/test_engine_pytest.py -v -m castling
Run with board printout:    pytest tests/test_engine_pytest.py -v -s

Sections:
    TestOpeningsAndBasicMoves   (15 tests)
    TestPieceMovement           (22 tests)
    TestCheckDetection          (14 tests)
    TestCheckmatePatterns       (22 tests)
    TestStalemateDraw           ( 9 tests)
    TestCastling                (23 tests)
    TestEnPassant               (13 tests)
    TestPins                    (12 tests)
    TestTacticsAndMisc          (20 tests)
"""

import pytest
from board import Board
from piece import King, Queen, Rook, Bishop, Knight, Pawn
from conftest import place_piece, make_move, compute_moves


# =================================================================
#  SECTION 1: Opening Positions & Basic Moves
# =================================================================
@pytest.mark.openings
class TestOpeningsAndBasicMoves:
    """Tests 1-15: Starting position, piece counts, and famous openings."""

    def test_01_all_white_pawns_have_two_moves(self, board_with_pieces):
        board, history = board_with_pieces
        for file in "abcdefgh":
            pawn = board.board_get_square(file + "2").piece_on_square
            assert pawn is not None and len(pawn.valid_moves) == 2

    def test_02_all_black_pawns_have_two_moves(self, board_with_pieces):
        board, history = board_with_pieces
        for file in "abcdefgh":
            pawn = board.board_get_square(file + "7").piece_on_square
            assert pawn is not None and len(pawn.valid_moves) == 2

    def test_03_white_has_20_moves_at_start(self, board_with_pieces):
        board, history = board_with_pieces
        total = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col].piece_on_square
                if piece is not None and piece.colour == 'w':
                    total += len(piece.valid_moves)
        assert total == 20

    def test_04_italian_game_bishop_reaches_c4(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "g1", "f3", history)
        make_move(board, "b8", "c6", history)
        make_move(board, "f1", "c4", history)
        board.print_board_state()
        bishop = board.board_get_square("c4").piece_on_square
        assert bishop is not None and bishop.__str__() == "BW"

    def test_05_pawn_blocked_cannot_advance(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        board.print_board_state()
        pawn = board.board_get_square("e4").piece_on_square
        assert "e5" not in pawn.valid_moves

    def test_06_black_has_20_moves_at_start(self, board_with_pieces):
        board, history = board_with_pieces
        total = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col].piece_on_square
                if piece is not None and piece.colour == 'b':
                    total += len(piece.valid_moves)
        assert total == 20

    def test_07_sicilian_defense(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "c7", "c5", history)
        board.print_board_state()
        pawn = board.board_get_square("c5").piece_on_square
        assert pawn is not None and pawn.__str__() == "PB"

    def test_08_queens_gambit_c4_can_capture_d5(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "d2", "d4", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "c2", "c4", history)
        board.print_board_state()
        pawn_c4 = board.board_get_square("c4").piece_on_square
        assert "d5" in pawn_c4.valid_moves

    def test_09_queens_gambit_d5_can_capture_c4(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "d2", "d4", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "c2", "c4", history)
        pawn_d5 = board.board_get_square("d5").piece_on_square
        assert "c4" in pawn_d5.valid_moves

    def test_10_e2_empty_after_e4(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        board.print_board_state()
        assert board.board_get_square("e2").piece_on_square is None

    def test_11_e4_pawn_lost_double_push(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        pawn = board.board_get_square("e4").piece_on_square
        assert "e6" not in pawn.valid_moves

    def test_12_ruy_lopez_bishop_b5(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "g1", "f3", history)
        make_move(board, "b8", "c6", history)
        make_move(board, "f1", "b5", history)
        board.print_board_state()
        bishop = board.board_get_square("b5").piece_on_square
        assert bishop is not None and bishop.__str__() == "BW"

    def test_13_both_kings_zero_moves_at_start(self, board_with_pieces):
        board, history = board_with_pieces
        wk = board.board_get_square("e1").piece_on_square
        bk = board.board_get_square("e8").piece_on_square
        assert len(wk.valid_moves) == 0 and len(bk.valid_moves) == 0

    def test_14_white_bishops_zero_moves_at_start(self, board_with_pieces):
        board, history = board_with_pieces
        bc = board.board_get_square("c1").piece_on_square
        bf = board.board_get_square("f1").piece_on_square
        assert len(bc.valid_moves) == 0 and len(bf.valid_moves) == 0

    def test_15_white_queen_zero_moves_at_start(self, board_with_pieces):
        board, history = board_with_pieces
        queen = board.board_get_square("d1").piece_on_square
        assert len(queen.valid_moves) == 0


# =================================================================
#  SECTION 2: Piece Movement Validation
# =================================================================
class TestPieceMovement:
    """Tests 16-37: Movement rules for every piece type."""

    def test_16_rook_straight_lines(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "d4")
        compute_moves(board, history)
        board.print_board_state()
        rook = board.board_get_square("d4").piece_on_square
        assert "d8" in rook.valid_moves and "h4" in rook.valid_moves
        assert "d1" in rook.valid_moves and "a4" in rook.valid_moves

    def test_17_rook_no_diagonal(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "d4")
        compute_moves(board, history)
        rook = board.board_get_square("d4").piece_on_square
        assert "e5" not in rook.valid_moves and "c3" not in rook.valid_moves

    def test_18_bishop_diagonal_only(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Bishop('w'), "d4")
        compute_moves(board, history)
        board.print_board_state()
        bishop = board.board_get_square("d4").piece_on_square
        assert "g7" in bishop.valid_moves and "a7" in bishop.valid_moves and "f2" in bishop.valid_moves

    def test_19_bishop_no_straight(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Bishop('w'), "d4")
        compute_moves(board, history)
        bishop = board.board_get_square("d4").piece_on_square
        assert "d8" not in bishop.valid_moves and "h4" not in bishop.valid_moves

    def test_20_queen_combines_rook_and_bishop(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Queen('w'), "d4")
        compute_moves(board, history)
        board.print_board_state()
        queen = board.board_get_square("d4").piece_on_square
        assert "d8" in queen.valid_moves and "g7" in queen.valid_moves
        assert "a4" in queen.valid_moves and "a7" in queen.valid_moves

    def test_21_knight_jumps_over_pieces(self, board_with_pieces):
        board, history = board_with_pieces
        board.print_board_state()
        knight = board.board_get_square("b1").piece_on_square
        assert "a3" in knight.valid_moves and "c3" in knight.valid_moves

    def test_22_knight_center_eight_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Knight('w'), "d4")
        compute_moves(board, history)
        board.print_board_state()
        knight = board.board_get_square("d4").piece_on_square
        assert len(knight.valid_moves) == 8

    def test_23_king_center_eight_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "d4")
        place_piece(board, King('b'), "a8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("d4").piece_on_square
        assert len(king.valid_moves) == 8

    def test_24_pawn_captures_diagonally(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Pawn('w'), "d4")
        place_piece(board, Pawn('b'), "e5")
        place_piece(board, Pawn('b'), "c5")
        compute_moves(board, history)
        board.print_board_state()
        pawn = board.board_get_square("d4").piece_on_square
        assert "c5" in pawn.valid_moves and "e5" in pawn.valid_moves

    def test_25_pawn_blocked_no_forward(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Pawn('w'), "d4")
        place_piece(board, Pawn('b'), "d5")
        compute_moves(board, history)
        board.print_board_state()
        pawn = board.board_get_square("d4").piece_on_square
        assert len(pawn.valid_moves) == 0

    def test_26_rook_corner_move_count(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('w'), "a1")
        compute_moves(board, history)
        board.print_board_state()
        rook = board.board_get_square("a1").piece_on_square
        assert len(rook.valid_moves) == 10

    def test_27_knight_corner_two_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Knight('w'), "a1")
        compute_moves(board, history)
        board.print_board_state()
        knight = board.board_get_square("a1").piece_on_square
        assert len(knight.valid_moves) == 2

    def test_28_knight_corner_targets(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Knight('w'), "a1")
        compute_moves(board, history)
        knight = board.board_get_square("a1").piece_on_square
        assert "b3" in knight.valid_moves and "c2" in knight.valid_moves

    def test_29_bishop_corner_long_diagonal(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Bishop('w'), "a1")
        compute_moves(board, history)
        board.print_board_state()
        bishop = board.board_get_square("a1").piece_on_square
        assert "g7" in bishop.valid_moves

    def test_30_queen_center_reaches_all_edges(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Queen('w'), "d4")
        compute_moves(board, history)
        board.print_board_state()
        queen = board.board_get_square("d4").piece_on_square
        assert "d8" in queen.valid_moves and "d1" in queen.valid_moves
        assert "h4" in queen.valid_moves and "a7" in queen.valid_moves
        assert "g1" in queen.valid_moves and "h8" in queen.valid_moves

    def test_31_rook_blocked_by_friendly(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('w'), "d1")
        place_piece(board, Bishop('w'), "d4")
        compute_moves(board, history)
        board.print_board_state()
        rook = board.board_get_square("d1").piece_on_square
        assert "d5" not in rook.valid_moves and "d4" not in rook.valid_moves

    def test_32_rook_can_reach_before_block(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('w'), "d1")
        place_piece(board, Bishop('w'), "d4")
        compute_moves(board, history)
        rook = board.board_get_square("d1").piece_on_square
        assert "d2" in rook.valid_moves and "d3" in rook.valid_moves

    def test_33_black_pawn_moves_downward(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Pawn('b'), "e7")
        compute_moves(board, history)
        board.print_board_state()
        pawn = board.board_get_square("e7").piece_on_square
        assert "e6" in pawn.valid_moves and "e5" in pawn.valid_moves

    def test_34_black_pawn_cannot_go_backward(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Pawn('b'), "e7")
        compute_moves(board, history)
        pawn = board.board_get_square("e7").piece_on_square
        assert "e8" not in pawn.valid_moves

    def test_35_pawn_three_options(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Pawn('w'), "d4")
        place_piece(board, Pawn('b'), "c5")
        place_piece(board, Pawn('b'), "e5")
        compute_moves(board, history)
        board.print_board_state()
        pawn = board.board_get_square("d4").piece_on_square
        assert len(pawn.valid_moves) == 3

    def test_36_knight_edge_four_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Knight('w'), "a4")
        compute_moves(board, history)
        board.print_board_state()
        knight = board.board_get_square("a4").piece_on_square
        assert len(knight.valid_moves) == 4

    def test_37_kings_cannot_be_adjacent(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "d4")
        place_piece(board, King('b'), "d6")
        compute_moves(board, history)
        board.print_board_state()
        wk = board.board_get_square("d4").piece_on_square
        assert "d5" not in wk.valid_moves


# =================================================================
#  SECTION 3: Check Detection
# =================================================================
@pytest.mark.check
class TestCheckDetection:
    """Tests 38-51: Various check scenarios."""

    def test_38_rook_check_along_rank(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "d8")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_39_double_check_rook_and_bishop(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('w'), "e1")
        place_piece(board, Bishop('w'), "b5")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_40_pawn_gives_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Pawn('w'), "d7")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_41_interposition_blocks_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "e7")
        place_piece(board, Rook('w'), "e4")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is False

    def test_42_king_cant_move_into_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('w'), "d1")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e8").piece_on_square
        assert "d8" not in king.valid_moves and "d7" not in king.valid_moves

    def test_43_knight_delivers_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Knight('w'), "d6")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_44_bishop_check_long_diagonal(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Bishop('w'), "c3")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_45_queen_check_along_file(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "d8")
        place_piece(board, Queen('w'), "d1")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_46_black_pawn_checks_white_king(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Pawn('b'), "f5")
        compute_moves(board, history)
        board.print_board_state()
        assert board.white_king_check is True

    def test_47_friendly_piece_blocks_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('w'), "e3")
        place_piece(board, Pawn('w'), "e5")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is False

    def test_48_rook_check_same_rank(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "a1")
        compute_moves(board, history)
        board.print_board_state()
        assert board.white_king_check is True

    def test_49_king_in_check_cant_stay_on_file(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "e2" not in king.valid_moves

    def test_50_king_in_check_has_escape(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        king = board.board_get_square("e1").piece_on_square
        has_escape = "d1" in king.valid_moves or "f1" in king.valid_moves or \
                     "d2" in king.valid_moves or "f2" in king.valid_moves
        assert has_escape

    def test_51_pawn_check_other_diagonal(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Pawn('w'), "f7")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True


# =================================================================
#  SECTION 4: Checkmate Patterns
# =================================================================
@pytest.mark.checkmate
class TestCheckmatePatterns:
    """Tests 52-73: Various checkmate and non-checkmate patterns."""

    def test_52_queen_king_mate_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "f6")
        place_piece(board, Queen('w'), "g7")
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_53_queen_king_mate_no_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "f6")
        place_piece(board, Queen('w'), "g7")
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        assert board.black_has_moves() is False

    def test_54_ladder_mate_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, Rook('w'), "a7")
        place_piece(board, Rook('w'), "b8")
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_55_ladder_mate_no_escape(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, Rook('w'), "a7")
        place_piece(board, Rook('w'), "b8")
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        assert board.black_has_moves() is False

    def test_56_fools_mate_in_check(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "f2", "f3", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "g2", "g4", history)
        make_move(board, "d8", "h4", history)
        board.print_board_state()
        assert board.white_king_check is True

    def test_57_fools_mate_no_moves(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "f2", "f3", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "g2", "g4", history)
        make_move(board, "d8", "h4", history)
        assert board.white_has_moves() is False

    def test_58_scholars_mate_in_check(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "f1", "c4", history)
        make_move(board, "b8", "c6", history)
        make_move(board, "d1", "h5", history)
        make_move(board, "g8", "f6", history)
        make_move(board, "h5", "f7", history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_59_scholars_mate_no_moves(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "f1", "c4", history)
        make_move(board, "b8", "c6", history)
        make_move(board, "d1", "h5", history)
        make_move(board, "g8", "f6", history)
        make_move(board, "h5", "f7", history)
        assert board.black_has_moves() is False

    def test_60_back_rank_mate_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "g1")
        place_piece(board, Pawn('w'), "f2")
        place_piece(board, Pawn('w'), "g2")
        place_piece(board, Pawn('w'), "h2")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "d1")
        compute_moves(board, history)
        board.print_board_state()
        assert board.white_king_check is True

    def test_61_back_rank_mate_no_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "g1")
        place_piece(board, Pawn('w'), "f2")
        place_piece(board, Pawn('w'), "g2")
        place_piece(board, Pawn('w'), "h2")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "d1")
        compute_moves(board, history)
        assert board.white_has_moves() is False

    def test_62_smothered_mate_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('b'), "g8")
        place_piece(board, Pawn('b'), "g7")
        place_piece(board, Pawn('b'), "h7")
        place_piece(board, Knight('w'), "f7")
        place_piece(board, King('w'), "e1")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_63_smothered_mate_no_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('b'), "g8")
        place_piece(board, Pawn('b'), "g7")
        place_piece(board, Pawn('b'), "h7")
        place_piece(board, Knight('w'), "f7")
        place_piece(board, King('w'), "e1")
        compute_moves(board, history)
        assert board.black_has_moves() is False

    def test_64_queen_bishop_mate_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, Queen('w'), "g7")
        place_piece(board, Bishop('w'), "f6")
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_65_queen_bishop_mate_no_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, Queen('w'), "g7")
        place_piece(board, Bishop('w'), "f6")
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        assert board.black_has_moves() is False

    def test_66_two_rook_king_mate_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "f6")
        place_piece(board, Rook('w'), "a8")
        place_piece(board, Rook('w'), "a7")
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_67_two_rook_king_mate_no_escape(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "f6")
        place_piece(board, Rook('w'), "a8")
        place_piece(board, Rook('w'), "a7")
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        assert board.black_has_moves() is False

    def test_68_not_checkmate_king_captures(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "e8")
        place_piece(board, King('w'), "a1")
        place_piece(board, Rook('w'), "e7")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True and board.black_has_moves() is True

    def test_69_not_checkmate_piece_blocks(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "a5")
        place_piece(board, King('w'), "a1")
        place_piece(board, Rook('w'), "e1")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_has_moves() is True

    def test_70_two_bishops_king_mate_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "b6")
        place_piece(board, Bishop('w'), "c6")
        place_piece(board, Bishop('w'), "d6")
        place_piece(board, King('b'), "a8")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_71_two_bishops_king_mate_no_escape(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "b6")
        place_piece(board, Bishop('w'), "c6")
        place_piece(board, Bishop('w'), "d6")
        place_piece(board, King('b'), "a8")
        compute_moves(board, history)
        assert board.black_has_moves() is False

    def test_72_anastasia_mate_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "h8")
        place_piece(board, Pawn('b'), "g7")
        place_piece(board, Knight('w'), "e7")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('w'), "a1")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is True

    def test_73_anastasia_mate_no_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "h8")
        place_piece(board, Pawn('b'), "g7")
        place_piece(board, Knight('w'), "e7")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('w'), "a1")
        compute_moves(board, history)
        assert board.black_has_moves() is False


# =================================================================
#  SECTION 5: Stalemate / Draw
# =================================================================
@pytest.mark.stalemate
class TestStalemateDraw:
    """Tests 74-82: Stalemate and draw detection."""

    def test_74_classic_stalemate_not_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "h8")
        place_piece(board, King('w'), "f7")
        place_piece(board, Queen('w'), "g6")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is False

    def test_75_classic_stalemate_no_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "h8")
        place_piece(board, King('w'), "f7")
        place_piece(board, Queen('w'), "g6")
        compute_moves(board, history)
        assert board.black_has_moves() is False

    def test_76_not_stalemate_king_can_escape(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "h8")
        place_piece(board, King('w'), "f7")
        place_piece(board, Rook('w'), "a1")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_has_moves() is True

    def test_77_white_stalemate_not_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "a3")
        place_piece(board, Queen('b'), "b3")
        compute_moves(board, history)
        board.print_board_state()
        assert board.white_king_check is False

    def test_78_white_stalemate_no_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "a3")
        place_piece(board, Queen('b'), "b3")
        compute_moves(board, history)
        assert board.white_has_moves() is False

    def test_79_not_stalemate_pawn_can_move(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "h8")
        place_piece(board, Pawn('b'), "a7")
        place_piece(board, King('w'), "f7")
        place_piece(board, Queen('w'), "g6")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_has_moves() is True

    def test_80_edge_stalemate_not_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "a8")
        place_piece(board, King('w'), "c7")
        place_piece(board, Queen('w'), "b6")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_king_check is False

    def test_81_edge_stalemate_no_moves(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "a8")
        place_piece(board, King('w'), "c7")
        place_piece(board, Queen('w'), "b6")
        compute_moves(board, history)
        assert board.black_has_moves() is False

    def test_82_not_stalemate_has_escape(self, empty_board):
        board, history = empty_board
        place_piece(board, King('b'), "h8")
        place_piece(board, King('w'), "a1")
        place_piece(board, Rook('w'), "g1")
        place_piece(board, Rook('w'), "a6")
        compute_moves(board, history)
        board.print_board_state()
        assert board.black_has_moves() is True


# =================================================================
#  SECTION 6: Castling
# =================================================================
@pytest.mark.castling
class TestCastling:
    """Tests 83-105: Castling rights and execution."""

    def test_83_white_kingside_available(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "g1" in king.valid_moves

    def test_84_white_queenside_available(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "c1" in king.valid_moves

    def test_85_no_castle_after_king_moved(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        make_move(board, "e1", "f1", history)
        make_move(board, "e8", "d8", history)
        make_move(board, "f1", "e1", history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "g1" not in king.valid_moves

    def test_86_no_castle_after_rook_moved(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        make_move(board, "h1", "h2", history)
        make_move(board, "e8", "d8", history)
        make_move(board, "h2", "h1", history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "g1" not in king.valid_moves

    def test_87_no_castle_in_check(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "e5")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "g1" not in king.valid_moves

    def test_88_no_castle_through_attack(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "f8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "g1" not in king.valid_moves

    def test_89_no_castle_piece_blocking(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, Bishop('w'), "f1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "g1" not in king.valid_moves

    def test_90_black_kingside_available(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "h8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e8").piece_on_square
        assert "g8" in king.valid_moves

    def test_91_black_queenside_available(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "a8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e8").piece_on_square
        assert "c8" in king.valid_moves

    def test_92_execute_oo_king_on_g1(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        make_move(board, "e1", "g1", history)
        board.print_board_state()
        assert board.board_get_square("g1").piece_on_square.__str__() == "KW"

    def test_93_execute_oo_rook_on_f1(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        make_move(board, "e1", "g1", history)
        assert board.board_get_square("f1").piece_on_square.__str__() == "RW"

    def test_94_execute_oo_e1_empty(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        make_move(board, "e1", "g1", history)
        assert board.board_get_square("e1").piece_on_square is None

    def test_95_execute_oo_h1_empty(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        make_move(board, "e1", "g1", history)
        assert board.board_get_square("h1").piece_on_square is None

    def test_96_execute_ooo_king_on_c1(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        make_move(board, "e1", "c1", history)
        board.print_board_state()
        assert board.board_get_square("c1").piece_on_square.__str__() == "KW"

    def test_97_execute_ooo_rook_on_d1(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        make_move(board, "e1", "c1", history)
        assert board.board_get_square("d1").piece_on_square.__str__() == "RW"

    def test_98_execute_ooo_a1_empty(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        make_move(board, "e1", "c1", history)
        assert board.board_get_square("a1").piece_on_square is None

    def test_99_no_castle_queenside_knight_b1(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, Knight('w'), "b1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "c1" not in king.valid_moves

    def test_100_no_castle_queenside_d1_attacked(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "d8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "c1" not in king.valid_moves

    def test_101_can_castle_even_if_a1_attacked(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "a8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "c1" in king.valid_moves

    def test_102_black_executes_oo_king_on_g8(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "h8")
        compute_moves(board, history)
        make_move(board, "e1", "d1", history)
        make_move(board, "e8", "g8", history)
        board.print_board_state()
        assert board.board_get_square("g8").piece_on_square.__str__() == "KB"

    def test_103_black_executes_oo_rook_on_f8(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "h8")
        compute_moves(board, history)
        make_move(board, "e1", "d1", history)
        make_move(board, "e8", "g8", history)
        assert board.board_get_square("f8").piece_on_square.__str__() == "RB"

    def test_104_both_sides_castling_available(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "g1" in king.valid_moves and "c1" in king.valid_moves

    def test_105_no_castle_queenside_c1_attacked_by_bishop(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Bishop('b'), "a3")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "c1" not in king.valid_moves


# =================================================================
#  SECTION 7: En Passant
# =================================================================
@pytest.mark.en_passant
class TestEnPassant:
    """Tests 106-118: En passant availability, execution, and edge cases."""

    def test_106_white_ep_left(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "d7", "d5", history)
        board.print_board_state()
        pawn = board.board_get_square("e5").piece_on_square
        assert "d6" in pawn.valid_moves

    def test_107_white_ep_right(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "f7", "f5", history)
        board.print_board_state()
        pawn = board.board_get_square("e5").piece_on_square
        assert "f6" in pawn.valid_moves

    def test_108_ep_expired(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "a2", "a3", history)
        make_move(board, "a6", "a5", history)
        board.print_board_state()
        pawn = board.board_get_square("e5").piece_on_square
        assert "d6" not in pawn.valid_moves

    def test_109_black_ep(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "a2", "a3", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "a3", "a4", history)
        make_move(board, "d5", "d4", history)
        make_move(board, "e2", "e4", history)
        board.print_board_state()
        pawn = board.board_get_square("d4").piece_on_square
        assert "e3" in pawn.valid_moves

    def test_110_ep_execute_pawn_on_target(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "e5", "d6", history)
        board.print_board_state()
        assert board.board_get_square("d6").piece_on_square.__str__() == "PW"

    def test_111_ep_execute_captured_pawn_removed(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "e5", "d6", history)
        assert board.board_get_square("d5").piece_on_square is None

    def test_112_ep_execute_origin_empty(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "e5", "d6", history)
        assert board.board_get_square("e5").piece_on_square is None

    def test_113_black_ep_left(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "a2", "a3", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "a3", "a4", history)
        make_move(board, "e5", "e4", history)
        make_move(board, "d2", "d4", history)
        board.print_board_state()
        pawn = board.board_get_square("e4").piece_on_square
        assert "d3" in pawn.valid_moves

    def test_114_no_ep_single_push(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "d7", "d6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "d6", "d5", history)
        board.print_board_state()
        pawn = board.board_get_square("e5").piece_on_square
        assert "d6" not in pawn.valid_moves

    def test_115_ep_a_file_edge(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "a2", "a4", history)
        make_move(board, "h7", "h6", history)
        make_move(board, "a4", "a5", history)
        make_move(board, "b7", "b5", history)
        board.print_board_state()
        pawn = board.board_get_square("a5").piece_on_square
        assert "b6" in pawn.valid_moves

    def test_116_ep_h_file_edge(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "h2", "h4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "h4", "h5", history)
        make_move(board, "g7", "g5", history)
        board.print_board_state()
        pawn = board.board_get_square("h5").piece_on_square
        assert "g6" in pawn.valid_moves

    def test_117_black_ep_execute_pawn_on_target(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "a2", "a3", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "a3", "a4", history)
        make_move(board, "d5", "d4", history)
        make_move(board, "e2", "e4", history)
        make_move(board, "d4", "e3", history)
        board.print_board_state()
        assert board.board_get_square("e3").piece_on_square.__str__() == "PB"

    def test_118_black_ep_execute_captured_removed(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "a2", "a3", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "a3", "a4", history)
        make_move(board, "d5", "d4", history)
        make_move(board, "e2", "e4", history)
        make_move(board, "d4", "e3", history)
        assert board.board_get_square("e4").piece_on_square is None


# =================================================================
#  SECTION 8: Pins (Absolute Pins)
# =================================================================
@pytest.mark.pins
class TestPins:
    """Tests 119-130: Absolute pin scenarios."""

    def test_119_knight_pinned_by_rook(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Knight('w'), "e4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        board.print_board_state()
        knight = board.board_get_square("e4").piece_on_square
        assert len(knight.valid_moves) == 0

    def test_120_pawn_pinned_by_bishop(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Pawn('w'), "d2")
        place_piece(board, King('b'), "a8")
        place_piece(board, Bishop('b'), "a5")
        compute_moves(board, history)
        board.print_board_state()
        pawn = board.board_get_square("d2").piece_on_square
        assert len(pawn.valid_moves) == 0

    def test_121_rook_pinned_moves_along_file(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "e4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        board.print_board_state()
        rook = board.board_get_square("e4").piece_on_square
        assert "e5" in rook.valid_moves and "e8" in rook.valid_moves

    def test_122_rook_pinned_cant_leave_file(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "e4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        rook = board.board_get_square("e4").piece_on_square
        assert "d4" not in rook.valid_moves and "f4" not in rook.valid_moves

    def test_123_bishop_pinned_along_pin_diagonal(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, Bishop('w'), "d4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Queen('b'), "g7")
        compute_moves(board, history)
        board.print_board_state()
        bishop = board.board_get_square("d4").piece_on_square
        assert "e5" in bishop.valid_moves and "f6" in bishop.valid_moves and "g7" in bishop.valid_moves

    def test_124_bishop_pinned_cant_leave_diagonal(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, Bishop('w'), "d4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Queen('b'), "g7")
        compute_moves(board, history)
        bishop = board.board_get_square("d4").piece_on_square
        assert "c5" not in bishop.valid_moves and "e3" not in bishop.valid_moves

    def test_125_queen_pinned_moves_along_file(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "d1")
        place_piece(board, Queen('w'), "d4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "d8")
        compute_moves(board, history)
        board.print_board_state()
        queen = board.board_get_square("d4").piece_on_square
        assert "d5" in queen.valid_moves and "d8" in queen.valid_moves

    def test_126_queen_pinned_cant_leave_file(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "d1")
        place_piece(board, Queen('w'), "d4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "d8")
        compute_moves(board, history)
        queen = board.board_get_square("d4").piece_on_square
        assert "c4" not in queen.valid_moves and "e4" not in queen.valid_moves

    def test_127_knight_pinned_on_diagonal(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, Knight('w'), "c3")
        place_piece(board, King('b'), "a8")
        place_piece(board, Bishop('b'), "f6")
        compute_moves(board, history)
        board.print_board_state()
        knight = board.board_get_square("c3").piece_on_square
        assert len(knight.valid_moves) == 0

    def test_128_pawn_pinned_on_file_can_advance(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Pawn('w'), "e2")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        board.print_board_state()
        pawn = board.board_get_square("e2").piece_on_square
        assert "e3" in pawn.valid_moves and "e4" in pawn.valid_moves

    def test_129_pinned_pawn_can_advance_on_file(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Pawn('w'), "e4")
        place_piece(board, Pawn('b'), "d5")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        board.print_board_state()
        pawn = board.board_get_square("e4").piece_on_square
        assert "e5" in pawn.valid_moves

    def test_130_pinned_pawn_cant_capture_off_line(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, Pawn('w'), "e4")
        place_piece(board, Pawn('b'), "d5")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        pawn = board.board_get_square("e4").piece_on_square
        assert "d5" not in pawn.valid_moves


# =================================================================
#  SECTION 9: X-Ray, Tactics & Miscellaneous
# =================================================================
@pytest.mark.tactics
class TestTacticsAndMisc:
    """Tests 131-150: Tactical patterns, captures, notation, and game flows."""

    def test_131_xray_rook_controls_full_file(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "e4")
        place_piece(board, Queen('w'), "e1")
        compute_moves(board, history)
        board.print_board_state()
        rook = board.board_get_square("e4").piece_on_square
        assert "e8" in rook.valid_moves

    def test_132_knight_fork_king_and_rook(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Knight('w'), "d6")
        place_piece(board, Rook('b'), "f7")
        compute_moves(board, history)
        board.print_board_state()
        knight = board.board_get_square("d6").piece_on_square
        assert "e8" in knight.valid_moves and "f7" in knight.valid_moves

    def test_133_knight_fork_king_and_queen(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Queen('b'), "c7")
        place_piece(board, Knight('w'), "d5")
        compute_moves(board, history)
        board.print_board_state()
        knight = board.board_get_square("d5").piece_on_square
        assert "c7" in knight.valid_moves

    def test_134_rook_open_file_full_control(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "d1")
        compute_moves(board, history)
        board.print_board_state()
        rook = board.board_get_square("d1").piece_on_square
        assert all(f"d{r}" in rook.valid_moves for r in range(2, 9))

    def test_135_battery_front_rook_sees_far_end(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "e1")
        place_piece(board, Rook('w'), "e4")
        compute_moves(board, history)
        board.print_board_state()
        front = board.board_get_square("e4").piece_on_square
        assert "e8" in front.valid_moves

    def test_136_battery_back_rook_blocked(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "e1")
        place_piece(board, Rook('w'), "e4")
        compute_moves(board, history)
        back = board.board_get_square("e1").piece_on_square
        assert "e4" not in back.valid_moves and "e3" in back.valid_moves

    def test_137_dark_bishop_controls_diagonal(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Bishop('w'), "c1")
        place_piece(board, Bishop('w'), "f1")
        compute_moves(board, history)
        board.print_board_state()
        dark = board.board_get_square("c1").piece_on_square
        assert "e3" in dark.valid_moves and "g5" in dark.valid_moves

    def test_138_light_bishop_controls_diagonal(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Bishop('w'), "c1")
        place_piece(board, Bishop('w'), "f1")
        compute_moves(board, history)
        light = board.board_get_square("f1").piece_on_square
        assert "e2" in light.valid_moves and "d3" in light.valid_moves

    def test_139_capture_places_piece(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "e4", "d5", history)
        board.print_board_state()
        assert board.board_get_square("d5").piece_on_square.__str__() == "PW"

    def test_140_capture_origin_empty(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "e4", "d5", history)
        assert board.board_get_square("e4").piece_on_square is None

    def test_141_capture_recorded(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "e4", "d5", history)
        assert len(board.captured_black_pawns) > 0

    def test_142_invalid_move_returns_minus_one(self, board_with_pieces):
        board, history = board_with_pieces
        result = make_move(board, "e2", "e5", history)
        assert result == -1

    def test_143_knight_notation_in_history(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "g1", "f3", history)
        board.print_board_state()
        assert "N" in history[-1] and "f3" in history[-1]

    def test_144_capture_notation_has_x(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "e4", "d5", history)
        assert "x" in history[-1]

    def test_145_board_reset_clears_pieces(self, board_with_pieces):
        board, history = board_with_pieces
        board.reset()
        for row in range(8):
            for col in range(8):
                assert board.board[row][col].piece_on_square is None

    def test_146_board_reset_clears_flags(self, board_with_pieces):
        board, history = board_with_pieces
        board.reset()
        assert board.black_king_check is False
        assert board.white_king_check is False
        assert board.black_king_checkmate is False
        assert board.white_king_checkmate is False
        assert board.draw is False

    def test_147_ruy_lopez_exchange_bishop_a4(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "g1", "f3", history)
        make_move(board, "b8", "c6", history)
        make_move(board, "f1", "b5", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "b5", "a4", history)
        board.print_board_state()
        assert board.board_get_square("a4").piece_on_square.__str__() == "BW"

    def test_148_ruy_lopez_no_checks(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "g1", "f3", history)
        make_move(board, "b8", "c6", history)
        make_move(board, "f1", "b5", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "b5", "a4", history)
        assert board.white_king_check is False and board.black_king_check is False

    def test_149_king_captures_undefended_piece(self, empty_board):
        board, history = empty_board
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "a8")
        place_piece(board, Knight('b'), "f2")
        compute_moves(board, history)
        board.print_board_state()
        king = board.board_get_square("e1").piece_on_square
        assert "f2" in king.valid_moves

    def test_150_giuoco_piano_mirror_bishops(self, board_with_pieces):
        board, history = board_with_pieces
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "g1", "f3", history)
        make_move(board, "b8", "c6", history)
        make_move(board, "f1", "c4", history)
        make_move(board, "f8", "c5", history)
        board.print_board_state()
        wb = board.board_get_square("c4").piece_on_square
        bb = board.board_get_square("c5").piece_on_square
        assert wb.__str__() == "BW" and bb.__str__() == "BB"

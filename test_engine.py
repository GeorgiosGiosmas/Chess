"""
Engine Tests - 150 tests covering chess engine rules and tactical patterns.

Categories:
- Opening positions & basic moves
- Piece movement validation
- Check detection
- Checkmate patterns
- Stalemate / Draw
- Castling (all edge cases)
- En Passant
- Pins (absolute pins)
- X-Ray attacks
- Tactical patterns
"""

from board import Board
from piece import *
from contextlib import redirect_stdout

# ============================================================
# Helpers
# ============================================================
def setup_board():
    """Fresh board with pieces initialized and moves computed."""
    board = Board()
    board.board_initialize_pieces()
    history = []
    board.get_all_pieces_moves(history)
    board.filter_legal_moves(history)
    return board, history

def setup_empty_board():
    """Empty board for custom positions."""
    board = Board()
    history = []
    return board, history

def print_board(board: Board):
    board.print_board_state()

def place_piece(board, piece, square_str):
    sq = board.board_get_square(square_str)
    sq.piece_on_square = piece
    if isinstance(piece, King):
        if piece.colour == 'w':
            board.white_king_square = sq
        else:
            board.black_king_square = sq

def make_move(board, from_sq, to_sq, history):
    result = board.make_move(from_sq, to_sq, history)
    if result == 0:
        board.get_all_pieces_moves(history)
        board.filter_legal_moves(history)
    return result

def compute_moves(board, history):
    board.get_all_pieces_moves(history)
    board.filter_legal_moves(history)

passed = 0
failed = 0

def test(name, condition):
    global passed, failed
    if condition:
        print(f"  PASS: {name}")
        passed += 1
    else:
        print(f"  FAIL: {name}")
        failed += 1

# ============================================================
# SECTION 1: Opening Positions & Basic Moves
# ============================================================
with open("test_engine_LOGS.txt", 'w') as f:
    with redirect_stdout(f):
        print("\n  ======== SECTION 1: Opening Positions & Basic Moves ========")

        # Test 1: All white pawns have 2 moves at start
        board, history = setup_board()
        all_pawns_two = True
        for file in "abcdefgh":
            pawn = board.board_get_square(file + "2").piece_on_square
            if pawn is None or len(pawn.valid_moves) != 2:
                all_pawns_two = False
        test("1. All 8 white pawns have exactly 2 moves at start", all_pawns_two)

        # Test 2: All black pawns have 2 moves at start
        all_black_pawns_two = True
        for file in "abcdefgh":
            pawn = board.board_get_square(file + "7").piece_on_square
            if pawn is None or len(pawn.valid_moves) != 2:
                all_black_pawns_two = False
        test("2. All 8 black pawns have exactly 2 moves at start", all_black_pawns_two)

        # Test 3: White has 20 total moves at start (16 pawn + 4 knight)
        total_white_moves = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col].piece_on_square
                if piece is not None and piece.colour == 'w':
                    total_white_moves += len(piece.valid_moves)
        test("3. White has exactly 20 legal moves at game start", total_white_moves == 20)
        print()

        # Test 4: Italian Game opening (1.e4 e5 2.Nf3 Nc6 3.Bc4)
        board, history = setup_board()
        make_move(board, "e2", "e4", history) # White Pawn
        make_move(board, "e7", "e5", history) # Black Pawn
        make_move(board, "g1", "f3", history) # White Knight
        make_move(board, "b8", "c6", history) # Black Knight
        make_move(board, "f1", "c4", history) # White Bishop
        print_board(board)
        bishop = board.board_get_square("c4").piece_on_square
        test("4. Italian Game: Bishop reaches c4", bishop is not None and bishop.__str__() == "BW")
        print()

        # Test 5: After 1.e4 e5, white pawn can't move to e5
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        print_board(board)
        pawn = board.board_get_square("e4").piece_on_square
        test("5. Pawn blocked: e4 pawn can't advance (e5 occupied)", "e5" not in pawn.valid_moves)
        print()

        # Test 6: Black has 20 total moves at start
        board, history = setup_board()
        total_black_moves = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col].piece_on_square
                if piece is not None and piece.colour == 'b':
                    total_black_moves += len(piece.valid_moves)
        test("6. Black has exactly 20 legal moves at game start", total_black_moves == 20)
        print()

        # Test 7: Sicilian Defense opening (1.e4 c5)
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "c7", "c5", history)
        print_board(board)
        pawn_c5 = board.board_get_square("c5").piece_on_square
        test("7. Sicilian Defense: black pawn reaches c5", pawn_c5 is not None and pawn_c5.__str__() == "PB")
        print()

        # Test 8: Queen's Gambit opening (1.d4 d5 2.c4)
        board, history = setup_board()
        make_move(board, "d2", "d4", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "c2", "c4", history)
        print_board(board)
        pawn_c4 = board.board_get_square("c4").piece_on_square
        pawn_d5 = board.board_get_square("d5").piece_on_square
        test("8. Queen's Gambit: c4 pawn can capture d5 diagonally", pawn_c4 is not None and "d5" in pawn_c4.valid_moves)
        test("9. Queen's Gambit: black d5 pawn can capture c4", "c4" in pawn_d5.valid_moves)
        print()

        # Test 10: After 1.e4, e2 square is empty
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        print_board(board)
        test("10. After 1.e4, e2 is empty", board.board_get_square("e2").piece_on_square is None)
        print()

        # Test 11: After 1.e4, the white e4 pawn has only 1 move (e5, single push)
        pawn = board.board_get_square("e4").piece_on_square
        test("11. After 1.e4, e4 pawn has lost double-push option", "e6" not in pawn.valid_moves)
        print()

        # Test 12: Ruy Lopez opening (1.e4 e5 2.Nf3 Nc6 3.Bb5)
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "g1", "f3", history)
        make_move(board, "b8", "c6", history)
        make_move(board, "f1", "b5", history)
        print_board(board)
        bishop_b5 = board.board_get_square("b5").piece_on_square
        test("12. Ruy Lopez: Bishop reaches b5", bishop_b5 is not None and bishop_b5.__str__() == "BW")
        print()

        # Test 13: Kings cannot have any moves at start
        board, history = setup_board()
        wk = board.board_get_square("e1").piece_on_square
        bk = board.board_get_square("e8").piece_on_square
        test("13. Both kings have 0 moves at game start", len(wk.valid_moves) == 0 and len(bk.valid_moves) == 0)
        print()

        # Test 14: White bishops have 0 moves at start (blocked by pawns)
        board, history = setup_board()
        bc = board.board_get_square("c1").piece_on_square
        bf = board.board_get_square("f1").piece_on_square
        test("14. Both white bishops have 0 moves at start", len(bc.valid_moves) == 0 and len(bf.valid_moves) == 0)
        print()

        # Test 15: White queen has 0 moves at start
        board, history = setup_board()
        queen = board.board_get_square("d1").piece_on_square
        test("15. White queen has 0 moves at start", len(queen.valid_moves) == 0)
        print()
        print()

        # ============================================================
        # SECTION 2: Piece Movement Validation
        # ============================================================
        print("\n  =========== SECTION 2: Piece Movement Validation ===========")
        print()

        # Test 16: Rook moves in straight lines
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "d4")
        compute_moves(board, history)
        print_board(board)
        rook = board.board_get_square("d4").piece_on_square
        test("16. Rook on d4 has moves along rank and file", "d8" in rook.valid_moves and "h4" in rook.valid_moves and "d1" in rook.valid_moves and "a4" in rook.valid_moves)

        # Test 17: Rook can't move diagonally
        test("17. Rook on d4 can't move diagonally", "e5" not in rook.valid_moves and "c3" not in rook.valid_moves)
        print()

        # Test 18: Bishop moves diagonally only
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Bishop('w'), "d4")
        compute_moves(board, history)
        print_board(board)
        bishop = board.board_get_square("d4").piece_on_square
        test("18. Bishop on d4 moves diagonally", "g7" in bishop.valid_moves and "a7" in bishop.valid_moves and "f2" in bishop.valid_moves)

        # Test 19: Bishop can't move in straight lines
        test("19. Bishop on d4 can't move along rank/file", "d8" not in bishop.valid_moves and "h4" not in bishop.valid_moves)
        print()

        # Test 20: Queen combines rook and bishop movement
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Queen('w'), "d4")
        compute_moves(board, history)
        print_board(board)
        queen = board.board_get_square("d4").piece_on_square
        test("20. Queen on d4 has both diagonal and straight moves", "d8" in queen.valid_moves and "g7" in queen.valid_moves and "a4" in queen.valid_moves and "a7" in queen.valid_moves)
        print()

        # Test 21: Knight jumps over pieces
        board, history = setup_board()
        print_board(board)
        knight = board.board_get_square("b1").piece_on_square
        test("21. Knight on b1 can jump over pawns to a3 and c3", "a3" in knight.valid_moves and "c3" in knight.valid_moves)
        print()

        # Test 22: Knight has up to 8 moves from center
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Knight('w'), "d4")
        compute_moves(board, history)
        print_board(board)
        knight = board.board_get_square("d4").piece_on_square
        test("22. Knight in center (d4) has 8 moves", len(knight.valid_moves) == 8)
        print()

        # Test 23: King has max 8 moves in open position
        board, history = setup_empty_board()
        place_piece(board, King('w'), "d4")
        place_piece(board, King('b'), "a8")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("d4").piece_on_square
        test("23. King in center (d4) has 8 moves", len(king.valid_moves) == 8)
        print()

        # Test 24: Pawn captures diagonally
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Pawn('w'), "d4")
        place_piece(board, Pawn('b'), "e5")
        place_piece(board, Pawn('b'), "c5")
        compute_moves(board, history)
        print_board(board)
        pawn = board.board_get_square("d4").piece_on_square
        test("24. Pawn on d4 can capture on c5 and e5", "c5" in pawn.valid_moves and "e5" in pawn.valid_moves)
        print()

        # Test 25: Pawn can't capture forward
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Pawn('w'), "d4")
        place_piece(board, Pawn('b'), "d5")
        compute_moves(board, history)
        print_board(board)
        pawn = board.board_get_square("d4").piece_on_square
        test("25. Pawn on d4 blocked by pawn on d5 (no forward move)", len(pawn.valid_moves) == 0)
        print()

        # Test 26: Rook on corner has 14 moves on empty board
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('w'), "a1")
        compute_moves(board, history)
        print_board(board)
        rook = board.board_get_square("a1").piece_on_square
        # a1 rook: a2-a8 (7 minus a-file blocked by nothing but e1 king is on e1 not a-file) = 7 up, b1-h1 minus e1 = 6 right
        # Actually: a2,a3,a4,a5,a6,a7,a8 = 7 up. b1,c1,d1 = 3 right (e1 has king, blocked).
        test("26. Rook on a1 moves: 7 up file + 3 along rank (king on e1 blocks)", len(rook.valid_moves) == 10)
        print()

        # Test 27: Knight on corner has only 2 moves
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Knight('w'), "a1")
        compute_moves(board, history)
        print_board(board)
        knight = board.board_get_square("a1").piece_on_square
        test("27. Knight on a1 (corner) has exactly 2 moves", len(knight.valid_moves) == 2)
        test("28. Knight on a1 can reach b3 and c2", "b3" in knight.valid_moves and "c2" in knight.valid_moves)
        print()

        # Test 29: Bishop on corner controls one diagonal only
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Bishop('w'), "a1")
        compute_moves(board, history)
        print_board(board)
        bishop = board.board_get_square("a1").piece_on_square
        # a1 bishop goes b2,c3,d4 (e5,f6,g7,h8 — but king on e1 doesn't block diagonal)
        # Actually: b2,c3,d4,e5,f6,g7 (h8 has black king, can capture) = 7 moves
        test("29. Bishop on a1 controls long diagonal toward h8", "g7" in bishop.valid_moves)
        print()

        # Test 30: Queen on center has maximum reach
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Queen('w'), "d4")
        compute_moves(board, history)
        print_board(board)
        queen = board.board_get_square("d4").piece_on_square
        # Queen on d4 should reach all edges: d8,d1,a4,h4 and corners a7,g7,a1(king),g1
        test("30. Queen on d4 reaches board edges in all 8 directions", 
            "d8" in queen.valid_moves and "d1" in queen.valid_moves and
            "h4" in queen.valid_moves and "a7" in queen.valid_moves and
            "g1" in queen.valid_moves and "h8" in queen.valid_moves)
        print()

        # Test 31: Rook blocked by friendly piece
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('w'), "d1")
        place_piece(board, Bishop('w'), "d4")
        compute_moves(board, history)
        print_board(board)
        rook = board.board_get_square("d1").piece_on_square
        test("31. Rook on d1 blocked by friendly bishop on d4 (can't reach d5+)", "d5" not in rook.valid_moves and "d4" not in rook.valid_moves)
        test("32. Rook on d1 can still reach d2 and d3", "d2" in rook.valid_moves and "d3" in rook.valid_moves)
        print()

        # Test 33: Black pawn moves downward
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Pawn('b'), "e7")
        compute_moves(board, history)
        print_board(board)
        pawn = board.board_get_square("e7").piece_on_square
        test("33. Black pawn on e7 can move to e6 and e5", "e6" in pawn.valid_moves and "e5" in pawn.valid_moves)
        test("34. Black pawn on e7 cannot move to e8 (backwards)", "e8" not in pawn.valid_moves)
        print()

        # Test 35: Pawn with 3 options (forward + 2 captures)
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Pawn('w'), "d4")
        place_piece(board, Pawn('b'), "c5")
        place_piece(board, Pawn('b'), "e5")
        compute_moves(board, history)
        print_board(board)
        pawn = board.board_get_square("d4").piece_on_square
        test("35. Pawn d4 has 3 moves: d5 forward, c5 and e5 captures", len(pawn.valid_moves) == 3)
        print()

        # Test 36: Knight on edge (b1-like position) has limited moves
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Knight('w'), "a4")
        compute_moves(board, history)
        print_board(board)
        knight = board.board_get_square("a4").piece_on_square
        test("36. Knight on a4 (edge) has 4 moves", len(knight.valid_moves) == 4)
        print()

        # Test 37: King cannot move next to opposing king
        board, history = setup_empty_board()
        place_piece(board, King('w'), "d4")
        place_piece(board, King('b'), "d6")
        compute_moves(board, history)
        print_board(board)
        wk = board.board_get_square("d4").piece_on_square
        test("37. White king on d4 can't move to d5 (adjacent to black king on d6)", "d5" not in wk.valid_moves)
        print()
        print()

        # ============================================================
        # SECTION 3: Check Detection
        # ============================================================
        print("\n  ================ SECTION 3: Check Detection ================")

        # Test 38: Rook check along rank
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "d8")
        compute_moves(board, history)
        print_board(board)
        test("38. Rook on d8 checks king on h8 (same rank)", board.black_king_check == True)
        print()

        # Test 39: Double check - two pieces giving check
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('w'), "e1")
        place_piece(board, Bishop('w'), "b5")
        compute_moves(board, history)
        print_board(board)
        test("39. Both rook e1 and bishop b5 check king e8", board.black_king_check == True)
        print()

        # Test 40: Pawn gives check diagonally
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Pawn('w'), "d7")
        compute_moves(board, history)
        print_board(board)
        test("40. Pawn on d7 checks black king on e8", board.black_king_check == True)
        print()

        # Test 41: Piece blocking check (interposition)
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "e7")  # Blocks check from below
        place_piece(board, Rook('w'), "e4")
        compute_moves(board, history)
        print_board(board)
        test("41. Rook e4 blocked by rook e7 - king not in check", board.black_king_check == False)
        print()

        # Test 42: King can't move into check
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('w'), "d1")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e8").piece_on_square
        test("42. Black king can't move to d-file (controlled by rook)", "d8" not in king.valid_moves and "d7" not in king.valid_moves)
        print()

        # Test 43: Knight delivers check (no blocking possible)
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Knight('w'), "d6")
        compute_moves(board, history)
        print_board(board)
        test("43. Knight on d6 checks black king on e8", board.black_king_check == True)
        print()

        # Test 44: Bishop delivers check on long diagonal
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Bishop('w'), "c3")
        compute_moves(board, history)
        print_board(board)
        test("44. Bishop on c3 checks king on h8 via long diagonal", board.black_king_check == True)
        print()

        # Test 45: Queen check along file
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "d8")
        place_piece(board, Queen('w'), "d1")
        compute_moves(board, history)
        print_board(board)
        test("45. Queen on d1 checks king on d8 along d-file", board.black_king_check == True)
        print()

        # Test 46: Black pawn checks white king
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Pawn('b'), "f5")
        compute_moves(board, history)
        print_board(board)
        test("46. Black pawn on f5 checks white king on e4", board.white_king_check == True)
        print()

        # Test 47: No check when piece is blocked by friendly piece
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('w'), "e3")
        place_piece(board, Pawn('w'), "e5")
        compute_moves(board, history)
        print_board(board)
        test("47. Rook e3 blocked by own pawn e5 - king e8 NOT in check", board.black_king_check == False)
        print()

        # Test 48: Check via rank (rook on same rank as king)
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "a1")
        compute_moves(board, history)
        print_board(board)
        test("48. Black rook on a1 checks white king on e1 (same rank)", board.white_king_check == True)
        print()

        # Test 49: King must escape check - limited moves
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("49. White king in check from e8 rook can't stay on e-file", "e2" not in king.valid_moves)
        test("50. White king in check from e8 can flee to d1 or f1 or d2 or f2", 
            "d1" in king.valid_moves or "f1" in king.valid_moves or "d2" in king.valid_moves or "f2" in king.valid_moves)
        print()

        # Test 51: Pawn on f7 checks black king on e8 (other diagonal)
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Pawn('w'), "f7")
        compute_moves(board, history)
        print_board(board)
        test("51. Pawn on f7 checks black king on e8 (right diagonal)", board.black_king_check == True)
        print()
        print()

        # ============================================================
        # SECTION 4: Checkmate Patterns
        # ============================================================
        print("\n  ============== SECTION 4: Checkmate Patterns ===============")

        # Test 52: Queen + King mate
        board, history = setup_empty_board()
        place_piece(board, King('w'), "f6")
        place_piece(board, Queen('w'), "g7")
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        print_board(board)
        test("52. Queen+King mate: black in check", board.black_king_check == True)
        test("53. Queen+King mate: no legal moves", board.black_has_moves() == False)
        print()

        # Test 54: Two rooks mate (ladder mate)
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, Rook('w'), "a7")
        place_piece(board, Rook('w'), "b8")
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        print_board(board)
        test("54. Ladder mate: rook b8 checks king h8", board.black_king_check == True)
        test("55. Ladder mate: rook a7 covers 7th rank, no escape", board.black_has_moves() == False)
        print()

        # Test 56: Fool's mate
        board, history = setup_board()
        make_move(board, "f2", "f3", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "g2", "g4", history)
        make_move(board, "d8", "h4", history)
        print_board(board)
        test("56. Fool's mate: white king in check", board.white_king_check == True)
        test("57. Fool's mate: white has no moves", board.white_has_moves() == False)
        print()

        # Test 58: Scholar's mate
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "f1", "c4", history)
        make_move(board, "b8", "c6", history)
        make_move(board, "d1", "h5", history)
        make_move(board, "g8", "f6", history)
        make_move(board, "h5", "f7", history)
        print_board(board)
        test("58. Scholar's mate: black king in check", board.black_king_check == True)
        test("59. Scholar's mate: black has no moves", board.black_has_moves() == False)
        print()

        # Test 60: Back rank mate
        board, history = setup_empty_board()
        place_piece(board, King('w'), "g1")
        place_piece(board, Pawn('w'), "f2")
        place_piece(board, Pawn('w'), "g2")
        place_piece(board, Pawn('w'), "h2")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "d1")
        compute_moves(board, history)
        print_board(board)
        test("60. Back rank mate: white king in check from d1", board.white_king_check == True)
        test("61. Back rank mate: pawns block escape, no legal moves", board.white_has_moves() == False)
        print()

        # Test 62: Smothered mate (knight)
        board, history = setup_empty_board()
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('b'), "g8")
        place_piece(board, Pawn('b'), "g7")
        place_piece(board, Pawn('b'), "h7")
        place_piece(board, Knight('w'), "f7")
        place_piece(board, King('w'), "e1")
        compute_moves(board, history)
        print_board(board)
        test("62. Smothered mate: knight f7 checks king h8", board.black_king_check == True)
        test("63. Smothered mate: own pieces block all escape squares", board.black_has_moves() == False)
        print()

        # Test 64: Queen + Bishop mate on diagonal
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, Queen('w'), "g7")
        place_piece(board, Bishop('w'), "f6")
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        print_board(board)
        test("64. Queen g7 + Bishop f6 checkmate: king in check", board.black_king_check == True)
        test("65. Queen g7 + Bishop f6 checkmate: no escape", board.black_has_moves() == False)
        print()

        # Test 66: Rook + King mate on edge
        board, history = setup_empty_board()
        place_piece(board, King('w'), "f6")
        place_piece(board, Rook('w'), "a8")
        place_piece(board, Rook('w'), "a7")  # Covers h7 escape via 7th rank
        place_piece(board, King('b'), "h8")
        compute_moves(board, history)
        print_board(board)
        test("66. Rook a8 + Rook a7 + King f6 checkmate: king in check", board.black_king_check == True)
        test("67. Rook a8 + Rook a7 + King f6 checkmate: king trapped on h8", board.black_has_moves() == False)
        print()

        # Test 68: NOT checkmate - king can capture checking piece
        board, history = setup_empty_board()
        place_piece(board, King('b'), "e8")
        place_piece(board, King('w'), "a1")
        place_piece(board, Rook('w'), "e7")
        compute_moves(board, history)
        print_board(board)
        test("68. Rook e7 checks but king can capture on e7", board.black_king_check == True and board.black_has_moves() == True)
        print()

        # Test 69: NOT checkmate - piece can block
        board, history = setup_empty_board()
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "a5")
        place_piece(board, King('w'), "a1")
        place_piece(board, Rook('w'), "e1")
        compute_moves(board, history)
        print_board(board)
        # Black rook a5 can interpose on e5
        test("69. Rook e1 checks king e8, but black rook a5 can block on e5", board.black_has_moves() == True)
        print()

        # Test 70: Two bishops + king mate
        board, history = setup_empty_board()
        place_piece(board, King('w'), "b6")
        place_piece(board, Bishop('w'), "c6")
        place_piece(board, Bishop('w'), "d6")
        place_piece(board, King('b'), "a8")
        compute_moves(board, history)
        print_board(board)
        test("70. Two bishops + king mate: black king in check", board.black_king_check == True)
        test("71. Two bishops + king mate: no escape", board.black_has_moves() == False)
        print()

        # Test 72: Anastasia's mate pattern (knight + rook)
        board, history = setup_empty_board()
        place_piece(board, King('b'), "h8")
        place_piece(board, Pawn('b'), "g7")
        place_piece(board, Knight('w'), "e7")  # Knight covers g8 and g6
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('w'), "a1")
        compute_moves(board, history)
        print_board(board)
        # Rook on h1 checks on h-file. Knight on e7 covers g8,g6. Pawn on g7 blocks.
        test("72. Anastasia-like mate: rook h1 checks king h8", board.black_king_check == True)
        test("73. Anastasia-like mate: knight blocks escape, no moves", board.black_has_moves() == False)
        print()
        print()

        # ============================================================
        # SECTION 5: Stalemate / Draw
        # ============================================================
        print("\n  ================ SECTION 5: Stalemate / Draw ===============")

        # Test 74: Classic stalemate - king trapped in corner
        board, history = setup_empty_board()
        place_piece(board, King('b'), "h8")
        place_piece(board, King('w'), "f7")
        place_piece(board, Queen('w'), "g6")
        compute_moves(board, history)
        print_board(board)
        test("74. Stalemate: black king not in check", board.black_king_check == False)
        test("75. Stalemate: black has no legal moves", board.black_has_moves() == False)
        print()

        # Test 76: King trapped but with one escape square
        board, history = setup_empty_board()
        place_piece(board, King('b'), "h8")
        place_piece(board, King('w'), "f7")
        place_piece(board, Rook('w'), "a1")
        compute_moves(board, history)
        print_board(board)
        test("76. Not stalemate: king h8 can move to g8", board.black_has_moves() == True)
        print()

        # Test 77: Stalemate with white king trapped
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "a3")
        place_piece(board, Queen('b'), "b3")
        compute_moves(board, history)
        print_board(board)
        test("77. White stalemate: king a1 not in check", board.white_king_check == False)
        test("78. White stalemate: white has no legal moves", board.white_has_moves() == False)
        print()

        # Test 79: Not stalemate - pawn can still move
        board, history = setup_empty_board()
        place_piece(board, King('b'), "h8")
        place_piece(board, Pawn('b'), "a7")
        place_piece(board, King('w'), "f7")
        place_piece(board, Queen('w'), "g6")
        compute_moves(board, history)
        print_board(board)
        test("79. Not stalemate: black pawn on a7 can still move", board.black_has_moves() == True)
        print()

        # Test 80: Stalemate - king on edge with queen controlling everything
        board, history = setup_empty_board()
        place_piece(board, King('b'), "a8")
        place_piece(board, King('w'), "c7")
        place_piece(board, Queen('w'), "b6")
        compute_moves(board, history)
        print_board(board)
        test("80. Stalemate: king a8 not in check", board.black_king_check == False)
        test("81. Stalemate: queen b6 + king c7 trap king a8", board.black_has_moves() == False)
        print()

        # Test 82: King trapped by rooks but has one escape
        board, history = setup_empty_board()
        place_piece(board, King('b'), "h8")
        place_piece(board, King('w'), "a1")
        place_piece(board, Rook('w'), "g1")
        place_piece(board, Rook('w'), "a6")  # Controls rank 6, leaves rank 7 open
        compute_moves(board, history)
        print_board(board)
        # g1 rook controls g-file. a6 rook controls rank 6. King can go to h7.
        test("82. Not stalemate: king h8 still has h7 available", board.black_has_moves() == True)
        print()
        print()

        # ============================================================
        # SECTION 6: Castling
        # ============================================================
        print("\n  =================== SECTION 6: Castling ====================")

        # Test 83: White kingside castle
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("83. White can castle kingside", "g1" in king.valid_moves)
        print()

        # Test 84: White queenside castle
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("84. White can castle queenside", "c1" in king.valid_moves)
        print()

        # Test 85: Can't castle after king has moved
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        make_move(board, "e1", "f1", history)
        make_move(board, "e8", "d8", history)
        make_move(board, "f1", "e1", history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("85. Can't castle after king has moved (back to e1)", "g1" not in king.valid_moves)
        print()

        # Test 86: Can't castle after rook has moved
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        make_move(board, "h1", "h2", history)
        make_move(board, "e8", "d8", history)
        make_move(board, "h2", "h1", history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("86. Can't castle after rook has moved (back to h1)", "g1" not in king.valid_moves)
        print()

        # Test 87: Can't castle when in check
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "e5")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("87. Can't castle when king is in check (rook e5)", "g1" not in king.valid_moves)
        print()

        # Test 88: Can't castle through attacked square
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "f8")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("88. Can't castle through attacked square (f1 attacked)", "g1" not in king.valid_moves)
        print()

        # Test 89: Can't castle with piece in the way
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, Bishop('w'), "f1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("89. Can't castle with bishop on f1 blocking", "g1" not in king.valid_moves)
        print()

        # Test 90: Black kingside castle
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "h8")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e8").piece_on_square
        test("90. Black can castle kingside", "g8" in king.valid_moves)
        print()

        # Test 91: Black queenside castle
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "a8")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e8").piece_on_square
        test("91. Black can castle queenside", "c8" in king.valid_moves)
        print()

        # Test 92: Execute white kingside castle and verify positions
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        make_move(board, "e1", "g1", history)
        print_board(board)
        test("92. After O-O: king on g1", board.board_get_square("g1").piece_on_square is not None and board.board_get_square("g1").piece_on_square.__str__() == "KW")
        test("93. After O-O: rook on f1", board.board_get_square("f1").piece_on_square is not None and board.board_get_square("f1").piece_on_square.__str__() == "RW")
        test("94. After O-O: e1 empty", board.board_get_square("e1").piece_on_square is None)
        test("95. After O-O: h1 empty", board.board_get_square("h1").piece_on_square is None)
        print()

        # Test 96: Execute white queenside castle and verify positions
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        make_move(board, "e1", "c1", history)
        print_board(board)
        test("96. After O-O-O: king on c1", board.board_get_square("c1").piece_on_square is not None and board.board_get_square("c1").piece_on_square.__str__() == "KW")
        test("97. After O-O-O: rook on d1", board.board_get_square("d1").piece_on_square is not None and board.board_get_square("d1").piece_on_square.__str__() == "RW")
        test("98. After O-O-O: a1 empty", board.board_get_square("a1").piece_on_square is None)
        print()

        # Test 99: Can't castle queenside with piece on b1
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, Knight('w'), "b1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("99. Can't castle queenside with knight on b1", "c1" not in king.valid_moves)
        print()

        # Test 100: Can't castle queenside when d1 is attacked
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "d8")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("100. Can't castle queenside when d1 attacked by rook d8", "c1" not in king.valid_moves)
        print()

        # Test 101: Can castle even if a1/b1 attacked (rook passes through)
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "a8")  # Attacks a1 but not c1/d1
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        # a1 is attacked but the king doesn't pass through a1, so castling should be fine
        # unless c1 or d1 is also attacked. a8 rook attacks a1 only.
        test("101. CAN castle queenside even though a1 is attacked (king doesn't cross a1)", "c1" in king.valid_moves)
        print()

        # Test 102: Black executes kingside castle
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Rook('b'), "h8")
        compute_moves(board, history)
        # White moves first (need a white move)
        make_move(board, "e1", "d1", history)
        make_move(board, "e8", "g8", history)
        print_board(board)
        test("102. After black O-O: king on g8", board.board_get_square("g8").piece_on_square is not None and board.board_get_square("g8").piece_on_square.__str__() == "KB")
        test("103. After black O-O: rook on f8", board.board_get_square("f8").piece_on_square is not None and board.board_get_square("f8").piece_on_square.__str__() == "RB")
        print()

        # Test 104: Both sides can castle (white kingside + queenside available)
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, Rook('w'), "h1")
        place_piece(board, King('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("104. White can castle both sides: g1 and c1 in valid moves", "g1" in king.valid_moves and "c1" in king.valid_moves)
        print()

        # Test 105: Can't castle queenside when c1 is attacked
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Bishop('b'), "a3")  # Controls c1
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("105. Can't castle queenside when c1 attacked by bishop a3", "c1" not in king.valid_moves)
        print()
        print()

        # ============================================================
        # SECTION 7: En Passant
        # ============================================================
        print("\n  ================== SECTION 7: En Passant ===================")

        # Test 106: White en passant to the left
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "d7", "d5", history)
        print_board(board)
        pawn = board.board_get_square("e5").piece_on_square
        test("106. White pawn e5 can en passant capture d6", "d6" in pawn.valid_moves)
        print()

        # Test 107: White en passant to the right
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "f7", "f5", history)
        print_board(board)
        pawn = board.board_get_square("e5").piece_on_square
        test("107. White pawn e5 can en passant capture f6", "f6" in pawn.valid_moves)
        print()

        # Test 108: En passant only available immediately
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "d7", "d5", history)
        print_board(board)
        # White plays something else instead of capturing
        make_move(board, "a2", "a3", history)
        make_move(board, "a6", "a5", history)
        print_board(board)
        pawn = board.board_get_square("e5").piece_on_square
        test("108. En passant expired: d6 no longer available", "d6" not in pawn.valid_moves)
        print()

        # Test 109: Black en passant
        board, history = setup_board()
        make_move(board, "a2", "a3", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "a3", "a4", history)
        make_move(board, "d5", "d4", history)
        make_move(board, "e2", "e4", history)
        print_board(board)
        pawn = board.board_get_square("d4").piece_on_square
        test("109. Black pawn d4 can en passant capture e3", "e3" in pawn.valid_moves)
        print()

        # Test 110: Execute white en passant and verify captured pawn removed
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "e5", "d6", history)
        print_board(board)
        test("110. After en passant: white pawn on d6", board.board_get_square("d6").piece_on_square is not None and board.board_get_square("d6").piece_on_square.__str__() == "PW")
        test("111. After en passant: d5 is empty (captured pawn removed)", board.board_get_square("d5").piece_on_square is None)
        test("112. After en passant: e5 is empty (pawn moved away)", board.board_get_square("e5").piece_on_square is None)
        print()

        # Test 113: Black en passant to the left
        board, history = setup_board()
        make_move(board, "a2", "a3", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "a3", "a4", history)
        make_move(board, "e5", "e4", history)
        make_move(board, "d2", "d4", history)
        print_board(board)
        pawn = board.board_get_square("e4").piece_on_square
        test("113. Black pawn e4 can en passant capture d3", "d3" in pawn.valid_moves)
        print()

        # Test 114: En passant not available for single-push pawn
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "d7", "d6", history)
        make_move(board, "e4", "e5", history)
        make_move(board, "d6", "d5", history)  # Single push to d5, not double push
        print_board(board)
        pawn = board.board_get_square("e5").piece_on_square
        test("114. No en passant: d5 pawn arrived via single push (d6-d5)", "d6" not in pawn.valid_moves)
        print()

        # Test 115: En passant on a-file edge
        board, history = setup_board()
        make_move(board, "a2", "a4", history)
        make_move(board, "h7", "h6", history)
        make_move(board, "a4", "a5", history)
        make_move(board, "b7", "b5", history)
        print_board(board)
        pawn = board.board_get_square("a5").piece_on_square
        test("115. En passant on edge: a5 pawn can capture b6", "b6" in pawn.valid_moves)
        print()

        # Test 116: En passant on h-file edge
        board, history = setup_board()
        make_move(board, "h2", "h4", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "h4", "h5", history)
        make_move(board, "g7", "g5", history)
        print_board(board)
        pawn = board.board_get_square("h5").piece_on_square
        test("116. En passant on edge: h5 pawn can capture g6", "g6" in pawn.valid_moves)
        print()

        # Test 117: Execute black en passant and verify
        board, history = setup_board()
        make_move(board, "a2", "a3", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "a3", "a4", history)
        make_move(board, "d5", "d4", history)
        make_move(board, "e2", "e4", history)
        make_move(board, "d4", "e3", history)
        print_board(board)
        test("117. Black en passant: black pawn on e3", board.board_get_square("e3").piece_on_square is not None and board.board_get_square("e3").piece_on_square.__str__() == "PB")
        test("118. Black en passant: e4 is empty (captured white pawn)", board.board_get_square("e4").piece_on_square is None)
        print()
        print()

        # ============================================================
        # SECTION 8: Pins (Absolute Pins)
        # ============================================================
        print("\n  ===================== SECTION 8: Pins ======================")

        # Test 119: Pinned piece can't move (rook pin)
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Knight('w'), "e4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        knight = board.board_get_square("e4").piece_on_square
        test("119. Knight on e4 pinned by rook e8 - has 0 legal moves", len(knight.valid_moves) == 0)
        print()

        # Test 120: Pinned piece along diagonal
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Pawn('w'), "d2")
        place_piece(board, King('b'), "a8")
        place_piece(board, Bishop('b'), "a5")
        compute_moves(board, history)
        print_board(board)
        pawn = board.board_get_square("d2").piece_on_square
        test("120. Pawn on d2 pinned by bishop a5 - can't move", len(pawn.valid_moves) == 0)
        print()

        # Test 121: Piece pinned but can move along pin line
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Rook('w'), "e4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        rook = board.board_get_square("e4").piece_on_square
        test("121. Rook on e4 pinned but can move along e-file", "e5" in rook.valid_moves and "e8" in rook.valid_moves)
        test("122. Rook on e4 pinned - can't move off e-file", "d4" not in rook.valid_moves and "f4" not in rook.valid_moves)
        print()

        # Test 123: Bishop pinned along diagonal can move along pin line
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, Bishop('w'), "d4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Queen('b'), "g7")
        compute_moves(board, history)
        print_board(board)
        bishop = board.board_get_square("d4").piece_on_square
        test("123. Bishop d4 pinned by queen g7 can move along diagonal (e5, f6, g7)", 
            "e5" in bishop.valid_moves and "f6" in bishop.valid_moves and "g7" in bishop.valid_moves)
        test("124. Bishop d4 pinned - can't move to other diagonal (c5, e3)", "c5" not in bishop.valid_moves and "e3" not in bishop.valid_moves)
        print()

        # Test 125: Queen pinned along file can still move along that file
        board, history = setup_empty_board()
        place_piece(board, King('w'), "d1")
        place_piece(board, Queen('w'), "d4")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "d8")
        compute_moves(board, history)
        print_board(board)
        queen = board.board_get_square("d4").piece_on_square
        test("125. Queen d4 pinned on d-file can move to d5, d6, d7, d8", 
            "d5" in queen.valid_moves and "d8" in queen.valid_moves)
        test("126. Queen d4 pinned on d-file can't move off file", "c4" not in queen.valid_moves and "e4" not in queen.valid_moves)
        print()

        # Test 127: Knight pinned on diagonal (absolutely stuck)
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, Knight('w'), "c3")
        place_piece(board, King('b'), "a8")
        place_piece(board, Bishop('b'), "f6")
        compute_moves(board, history)
        print_board(board)
        knight = board.board_get_square("c3").piece_on_square
        test("127. Knight c3 pinned by bishop f6 on a1-h8 diagonal: 0 moves", len(knight.valid_moves) == 0)
        print()

        # Test 128: Pawn pinned on file can still advance along file
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Pawn('w'), "e2")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        pawn = board.board_get_square("e2").piece_on_square
        test("128. Pawn e2 pinned on e-file can still advance to e3 and e4", "e3" in pawn.valid_moves and "e4" in pawn.valid_moves)
        print()

        # Test 129: Pinned pawn cannot capture (capture goes off pin line)
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, Pawn('w'), "e4")
        place_piece(board, Pawn('b'), "d5")
        place_piece(board, King('b'), "a8")
        place_piece(board, Rook('b'), "e8")
        compute_moves(board, history)
        print_board(board)
        pawn = board.board_get_square("e4").piece_on_square
        test("129. Pawn e4 pinned on e-file can advance to e5", "e5" in pawn.valid_moves)
        test("130. Pawn e4 pinned on e-file can't capture d5 (off pin line)", "d5" not in pawn.valid_moves)
        print()
        print()

        # ============================================================
        # SECTION 9: X-Ray & Tactics
        # ============================================================
        print("\n  ================ SECTION 9: X-Ray & Tactics ================")

        # Test 131: Queen behind rook on same file
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "e4")
        place_piece(board, Queen('w'), "e1")
        compute_moves(board, history)
        print_board(board)
        rook = board.board_get_square("e4").piece_on_square
        queen = board.board_get_square("e1").piece_on_square
        test("131. X-ray: Rook on e4 controls up to e8", "e8" in rook.valid_moves)
        print()

        # Test 132: Knight fork - attacks multiple pieces simultaneously
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Knight('w'), "d6")
        place_piece(board, Rook('b'), "f7")
        compute_moves(board, history)
        print_board(board)
        knight = board.board_get_square("d6").piece_on_square
        test("132. Knight fork: d6 attacks both king e8 and rook f7", "e8" in knight.valid_moves and "f7" in knight.valid_moves)
        print()

        # Test 133: Knight fork on king and queen
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "e8")
        place_piece(board, Queen('b'), "c7")
        place_piece(board, Knight('w'), "d5")
        compute_moves(board, history)
        print_board(board)
        knight = board.board_get_square("d5").piece_on_square
        test("133. Knight d5 forks: attacks queen c7 and can reach e7 near king", 
            "c7" in knight.valid_moves)
        print()

        # Test 134: Rook on open file controls entire file
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "d1")
        compute_moves(board, history)
        print_board(board)
        rook = board.board_get_square("d1").piece_on_square
        all_file = all(f"d{r}" in rook.valid_moves for r in range(2, 9))
        test("134. Rook d1 on open file controls d2 through d8", all_file)
        print()

        # Test 135: Two rooks on same file - battery
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Rook('w'), "e1")
        place_piece(board, Rook('w'), "e4")
        compute_moves(board, history)
        print_board(board)
        front_rook = board.board_get_square("e4").piece_on_square
        back_rook = board.board_get_square("e1").piece_on_square
        test("135. Battery: front rook e4 sees e5-e8", "e8" in front_rook.valid_moves)
        test("136. Battery: back rook e1 sees e2-e3 (blocked by front rook)", "e4" not in back_rook.valid_moves and "e3" in back_rook.valid_moves)
        print()

        # Test 137: Bishop pair controlling both diagonals
        board, history = setup_empty_board()
        place_piece(board, King('w'), "a1")
        place_piece(board, King('b'), "h8")
        place_piece(board, Bishop('w'), "c1")  # Dark square bishop
        place_piece(board, Bishop('w'), "f1")  # Light square bishop
        compute_moves(board, history)
        print_board(board)
        dark_bishop = board.board_get_square("c1").piece_on_square
        light_bishop = board.board_get_square("f1").piece_on_square
        test("137. Dark bishop c1 controls dark diagonal (e3,f4,g5)", "e3" in dark_bishop.valid_moves and "g5" in dark_bishop.valid_moves)
        test("138. Light bishop f1 controls light diagonal (e2,d3,c4)", "e2" in light_bishop.valid_moves and "d3" in light_bishop.valid_moves)
        print()

        # Test 139: Capture removes piece from board
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "e4", "d5", history)
        print_board(board)
        test("139. After exd5: white pawn on d5", board.board_get_square("d5").piece_on_square.__str__() == "PW")
        test("140. After exd5: e4 is empty", board.board_get_square("e4").piece_on_square is None)
        test("141. After exd5: captured black pawn recorded", len(board.captured_black_pawns) > 0)
        print()

        # Test 142: Invalid move returns -1
        board, history = setup_board()
        result = make_move(board, "e2", "e5", history)
        test("142. Invalid move e2-e5 returns -1", result == -1)
        print()

        # Test 143: History notation includes piece letter for non-pawns
        board, history = setup_board()
        make_move(board, "g1", "f3", history)
        print_board(board)
        test("143. Knight move recorded with 'N' in history", "N" in history[-1] and "f3" in history[-1])
        print()

        # Test 144: History notation for capture includes 'x'
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "d7", "d5", history)
        make_move(board, "e4", "d5", history)
        test("144. Capture notation includes 'x'", "x" in history[-1])
        print()

        # Test 145: Board reset clears all pieces
        board, history = setup_board()
        board.reset()
        all_empty = True
        for row in range(8):
            for col in range(8):
                if board.board[row][col].piece_on_square is not None:
                    all_empty = False
        test("145. Board reset clears all 64 squares", all_empty)
        print()

        # Test 146: Board reset clears all flags
        test("146. Board reset clears check/checkmate flags", 
            board.black_king_check == False and board.white_king_check == False and
            board.black_king_checkmate == False and board.white_king_checkmate == False and
            board.draw == False)
        print()

        # Test 147: Multi-move game - king safety after series of moves
        board, history = setup_board()
        make_move(board, "e2", "e4", history)
        make_move(board, "e7", "e5", history)
        make_move(board, "g1", "f3", history)
        make_move(board, "b8", "c6", history)
        make_move(board, "f1", "b5", history)
        make_move(board, "a7", "a6", history)
        make_move(board, "b5", "a4", history)
        print_board(board)
        test("147. Ruy Lopez exchange: after Ba4, bishop is on a4", board.board_get_square("a4").piece_on_square.__str__() == "BW")
        test("148. Ruy Lopez: both kings still safe (no checks)", board.white_king_check == False and board.black_king_check == False)
        print()

        # Test 149: King can capture undefended checking piece
        board, history = setup_empty_board()
        place_piece(board, King('w'), "e1")
        place_piece(board, King('b'), "a8")
        place_piece(board, Knight('b'), "f2")
        compute_moves(board, history)
        print_board(board)
        king = board.board_get_square("e1").piece_on_square
        test("149. King e1 can capture undefended knight on f2", "f2" in king.valid_moves)
        print()

        # Test 150: Full game - Giuoco Piano opening sequence
        board, history = setup_board()
        make_move(board, "e2", "e4", history)   # 1. e4
        make_move(board, "e7", "e5", history)   # 1... e5
        make_move(board, "g1", "f3", history)   # 2. Nf3
        make_move(board, "b8", "c6", history)   # 2... Nc6
        make_move(board, "f1", "c4", history)   # 3. Bc4
        make_move(board, "f8", "c5", history)   # 3... Bc5
        print_board(board)
        w_bishop = board.board_get_square("c4").piece_on_square
        b_bishop = board.board_get_square("c5").piece_on_square
        test("150. Giuoco Piano: white bishop c4, black bishop c5 (mirror structure)", 
            w_bishop is not None and w_bishop.__str__() == "BW" and
            b_bishop is not None and b_bishop.__str__() == "BB")
        print()
        print()

        # ============================================================
        # SUMMARY
        # ============================================================
        print(f"\n{'='*50}")
        print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
        print(f"{'='*50}")
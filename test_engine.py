"""
Engine Tests - 50 tests covering chess engine rules and tactical patterns.

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
print("\n  ======== SECTION 1: Opening Positions & Basic Moves ========")

# Test 1: All white pawns have 2 moves at start
board, history = setup_board()
all_pawns_two = True
for file in "abcdefgh":
    pawn = board.board_get_square(file + "2").piece_on_square
    if pawn is None or len(pawn.valid_moves) != 2:
        all_pawns_two = False
test("1. All 8 white pawns have exactly 2 moves at start", all_pawns_two)
print()

# Test 2: All black pawns have 2 moves at start
all_black_pawns_two = True
for file in "abcdefgh":
    pawn = board.board_get_square(file + "7").piece_on_square
    if pawn is None or len(pawn.valid_moves) != 2:
        all_black_pawns_two = False
test("2. All 8 black pawns have exactly 2 moves at start", all_black_pawns_two)
print()

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
print()

# ============================================================
# SECTION 2: Piece Movement Validation
# ============================================================
print("\n  =========== SECTION 2: Piece Movement Validation ===========")
print()

# Test 6: Rook moves in straight lines
board, history = setup_empty_board()
place_piece(board, King('w'), "a1")
place_piece(board, King('b'), "h8")
place_piece(board, Rook('w'), "d4")
compute_moves(board, history)
print_board(board)
rook = board.board_get_square("d4").piece_on_square
test("6. Rook on d4 has moves along rank and file", "d8" in rook.valid_moves and "h4" in rook.valid_moves and "d1" in rook.valid_moves and "a4" in rook.valid_moves)

# Test 7: Rook can't move diagonally
test("7. Rook on d4 can't move diagonally", "e5" not in rook.valid_moves and "c3" not in rook.valid_moves)
print()

# Test 8: Bishop moves diagonally only
board, history = setup_empty_board()
place_piece(board, King('w'), "a1")
place_piece(board, King('b'), "h8")
place_piece(board, Bishop('w'), "d4")
compute_moves(board, history)
print_board(board)
bishop = board.board_get_square("d4").piece_on_square
test("8. Bishop on d4 moves diagonally", "g7" in bishop.valid_moves and "a7" in bishop.valid_moves and "f2" in bishop.valid_moves)

# Test 9: Bishop can't move in straight lines
test("9. Bishop on d4 can't move along rank/file", "d8" not in bishop.valid_moves and "h4" not in bishop.valid_moves)
print()

# Test 10: Queen combines rook and bishop movement
board, history = setup_empty_board()
place_piece(board, King('w'), "a1")
place_piece(board, King('b'), "h8")
place_piece(board, Queen('w'), "d4")
compute_moves(board, history)
print_board(board)
queen = board.board_get_square("d4").piece_on_square
test("10. Queen on d4 has both diagonal and straight moves", "d8" in queen.valid_moves and "g7" in queen.valid_moves and "a4" in queen.valid_moves and "a7" in queen.valid_moves)
print()

# Test 11: Knight jumps over pieces
board, history = setup_board()
print_board(board)
knight = board.board_get_square("b1").piece_on_square
test("11. Knight on b1 can jump over pawns to a3 and c3", "a3" in knight.valid_moves and "c3" in knight.valid_moves)
print()

# Test 12: Knight has up to 8 moves from center
board, history = setup_empty_board()
place_piece(board, King('w'), "a1")
place_piece(board, King('b'), "h8")
place_piece(board, Knight('w'), "d4")
compute_moves(board, history)
print_board(board)
knight = board.board_get_square("d4").piece_on_square
test("12. Knight in center (d4) has 8 moves", len(knight.valid_moves) == 8)
print()

# Test 13: King has max 8 moves in open position
board, history = setup_empty_board()
place_piece(board, King('w'), "d4")
place_piece(board, King('b'), "a8")
compute_moves(board, history)
print_board(board)
king = board.board_get_square("d4").piece_on_square
test("13. King in center (d4) has 8 moves", len(king.valid_moves) == 8)
print()

# Test 14: Pawn captures diagonally
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, King('b'), "e8")
place_piece(board, Pawn('w'), "d4")
place_piece(board, Pawn('b'), "e5")
place_piece(board, Pawn('b'), "c5")
compute_moves(board, history)
print_board(board)
pawn = board.board_get_square("d4").piece_on_square
test("14. Pawn on d4 can capture on c5 and e5", "c5" in pawn.valid_moves and "e5" in pawn.valid_moves)
print()

# Test 15: Pawn can't capture forward
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, King('b'), "e8")
place_piece(board, Pawn('w'), "d4")
place_piece(board, Pawn('b'), "d5")
compute_moves(board, history)
print_board(board)
pawn = board.board_get_square("d4").piece_on_square
test("15. Pawn on d4 blocked by pawn on d5 (no forward move)", len(pawn.valid_moves) == 0)
print()
print()

# ============================================================
# SECTION 3: Check Detection
# ============================================================
print("\n  ================ SECTION 3: Check Detection ================")

# Test 16: Discovered check (bishop behind rook)
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, King('b'), "e8")
place_piece(board, Rook('w'), "e4")
place_piece(board, Bishop('w'), "e3")
compute_moves(board, history)
print_board(board)
# Move rook off the e-file to reveal bishop... but bishop on e3 is same file, not diagonal
# Let's use a proper discovered check setup
board, history = setup_empty_board()
place_piece(board, King('w'), "a1")
place_piece(board, King('b'), "h8")
place_piece(board, Rook('w'), "d8")
compute_moves(board, history)
print_board(board)
test("16. Rook on d8 checks king on h8 (same rank)", board.black_king_check == True)
print()

# Test 17: Double check concept - two pieces giving check
board, history = setup_empty_board()
place_piece(board, King('w'), "a1")
place_piece(board, King('b'), "e8")
place_piece(board, Rook('w'), "e1")
place_piece(board, Bishop('w'), "b5")
compute_moves(board, history)
print_board(board)
test("17. Both rook e1 and bishop b5 check king e8", board.black_king_check == True)
print()

# Test 18: Pawn gives check diagonally
board, history = setup_empty_board()
place_piece(board, King('w'), "a1")
place_piece(board, King('b'), "e8")
place_piece(board, Pawn('w'), "d7")
compute_moves(board, history)
print_board(board)
test("18. Pawn on d7 checks black king on e8", board.black_king_check == True)
print()

# Test 19: Piece blocking check (interposition)
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, King('b'), "e8")
place_piece(board, Rook('b'), "e7")  # Blocks check from below
place_piece(board, Rook('w'), "e4")
compute_moves(board, history)
print_board(board)
test("19. Rook e4 blocked by rook e7 - king not in check", board.black_king_check == False)
print()

# Test 20: King can't move into check
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, King('b'), "e8")
place_piece(board, Rook('w'), "d1")
compute_moves(board, history)
print_board(board)
king = board.board_get_square("e8").piece_on_square
test("20. Black king can't move to d-file (controlled by rook)", "d8" not in king.valid_moves and "d7" not in king.valid_moves)
print()
print()

# ============================================================
# SECTION 4: Checkmate Patterns
# ============================================================
print("\n  ============== SECTION 4: Checkmate Patterns ===============")

# Test 21: Queen + King mate
board, history = setup_empty_board()
place_piece(board, King('w'), "f6")
place_piece(board, Queen('w'), "g7")
place_piece(board, King('b'), "h8")
compute_moves(board, history)
print_board(board)
test("21. Queen+King mate: black in check", board.black_king_check == True)
test("22. Queen+King mate: no legal moves", board.black_has_moves() == False)
print()

# Test 23: Two rooks mate (ladder mate)
board, history = setup_empty_board()
place_piece(board, King('w'), "a1")
place_piece(board, Rook('w'), "a7")
place_piece(board, Rook('w'), "b8")
place_piece(board, King('b'), "h8")
compute_moves(board, history)
print_board(board)
test("23. Ladder mate: rook b8 checks king h8", board.black_king_check == True)
test("24. Ladder mate: rook a7 covers 7th rank, no escape", board.black_has_moves() == False)
print()

# Test 25: Fool's mate
board, history = setup_board()
make_move(board, "f2", "f3", history)
make_move(board, "e7", "e5", history)
make_move(board, "g2", "g4", history)
make_move(board, "d8", "h4", history)
print_board(board)
test("25. Fool's mate: white king in check", board.white_king_check == True)
test("26. Fool's mate: white has no moves", board.white_has_moves() == False)
print()

# Test 27: Scholar's mate
board, history = setup_board()
make_move(board, "e2", "e4", history)
make_move(board, "e7", "e5", history)
make_move(board, "f1", "c4", history)
make_move(board, "b8", "c6", history)
make_move(board, "d1", "h5", history)
make_move(board, "g8", "f6", history)
make_move(board, "h5", "f7", history)
print_board(board)
test("27. Scholar's mate: black king in check", board.black_king_check == True)
test("28. Scholar's mate: black has no moves", board.black_has_moves() == False)
print()
print()

# ============================================================
# SECTION 5: Stalemate / Draw
# ============================================================
print("\n  ================ SECTION 5: Stalemate / Draw ===============")

# Test 29: Classic stalemate - king trapped in corner
board, history = setup_empty_board()
place_piece(board, King('b'), "h8")
place_piece(board, King('w'), "f7")
place_piece(board, Queen('w'), "g6")
compute_moves(board, history)
print_board(board)
test("29. Stalemate: black king not in check", board.black_king_check == False)
test("30. Stalemate: black has no legal moves", board.black_has_moves() == False)
print()

# Test 31: King trapped but with one escape square
board, history = setup_empty_board()
place_piece(board, King('b'), "h8")
place_piece(board, King('w'), "f7")
place_piece(board, Rook('w'), "a1")
compute_moves(board, history)
print_board(board)
test("31. Not stalemate: king h8 can move to g8", board.black_has_moves() == True)
print()
print()

# ============================================================
# SECTION 6: Castling
# ============================================================
print("\n  =================== SECTION 6: Castling ====================")

# Test 32: White kingside castle
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, Rook('w'), "h1")
place_piece(board, King('b'), "e8")
compute_moves(board, history)
print_board(board)
king = board.board_get_square("e1").piece_on_square
test("32. White can castle kingside", "g1" in king.valid_moves)
print()

# Test 33: White queenside castle
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, Rook('w'), "a1")
place_piece(board, King('b'), "e8")
compute_moves(board, history)
print_board(board)
king = board.board_get_square("e1").piece_on_square
test("33. White can castle queenside", "c1" in king.valid_moves)
print()

# Test 34: Can't castle after king has moved
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
test("34. Can't castle after king has moved (back to e1)", "g1" not in king.valid_moves)
print()

# Test 35: Can't castle after rook has moved
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
test("35. Can't castle after rook has moved (back to h1)", "g1" not in king.valid_moves)
print()

# Test 36: Can't castle when in check
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, Rook('w'), "h1")
place_piece(board, King('b'), "e8")
place_piece(board, Rook('b'), "e5")
compute_moves(board, history)
print_board(board)
king = board.board_get_square("e1").piece_on_square
test("36. Can't castle when king is in check (rook e5)", "g1" not in king.valid_moves)
print()

# Test 37: Can't castle through attacked square
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, Rook('w'), "h1")
place_piece(board, King('b'), "e8")
place_piece(board, Rook('b'), "f8")
compute_moves(board, history)
print_board(board)
king = board.board_get_square("e1").piece_on_square
test("37. Can't castle through attacked square (f1 attacked)", "g1" not in king.valid_moves)
print()

# Test 38: Can't castle with piece in the way
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, Rook('w'), "h1")
place_piece(board, Bishop('w'), "f1")
place_piece(board, King('b'), "e8")
compute_moves(board, history)
print_board(board)
king = board.board_get_square("e1").piece_on_square
test("38. Can't castle with bishop on f1 blocking", "g1" not in king.valid_moves)
print()

# Test 39: Black kingside castle
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, King('b'), "e8")
place_piece(board, Rook('b'), "h8")
compute_moves(board, history)
print_board(board)
king = board.board_get_square("e8").piece_on_square
test("39. Black can castle kingside", "g8" in king.valid_moves)
print()

# Test 40: Black queenside castle
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, King('b'), "e8")
place_piece(board, Rook('b'), "a8")
compute_moves(board, history)
print_board(board)
king = board.board_get_square("e8").piece_on_square
test("40. Black can castle queenside", "c8" in king.valid_moves)
print()
print()

# ============================================================
# SECTION 7: En Passant
# ============================================================
print("\n  ================== SECTION 7: En Passant ===================")

# Test 41: White en passant to the left
board, history = setup_board()
make_move(board, "e2", "e4", history)
make_move(board, "a7", "a6", history)
make_move(board, "e4", "e5", history)
make_move(board, "d7", "d5", history)
print_board(board)
pawn = board.board_get_square("e5").piece_on_square
test("41. White pawn e5 can en passant capture d6", "d6" in pawn.valid_moves)
print()

# Test 42: White en passant to the right
board, history = setup_board()
make_move(board, "e2", "e4", history)
make_move(board, "a7", "a6", history)
make_move(board, "e4", "e5", history)
make_move(board, "f7", "f5", history)
print_board(board)
pawn = board.board_get_square("e5").piece_on_square
test("42. White pawn e5 can en passant capture f6", "f6" in pawn.valid_moves)
print()

# Test 43: En passant only available immediately
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
test("43. En passant expired: d6 no longer available", "d6" not in pawn.valid_moves)
print()

# Test 44: Black en passant
board, history = setup_board()
make_move(board, "a2", "a3", history)
make_move(board, "d7", "d5", history)
make_move(board, "a3", "a4", history)
make_move(board, "d5", "d4", history)
make_move(board, "e2", "e4", history)
print_board(board)
pawn = board.board_get_square("d4").piece_on_square
test("44. Black pawn d4 can en passant capture e3", "e3" in pawn.valid_moves)
print()
print()

# ============================================================
# SECTION 8: Pins (Absolute Pins)
# ============================================================
print("\n  ===================== SECTION 8: Pins ======================")

# Test 45: Pinned piece can't move (rook pin)
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, Knight('w'), "e4")
place_piece(board, King('b'), "a8")
place_piece(board, Rook('b'), "e8")
compute_moves(board, history)
print_board(board)
knight = board.board_get_square("e4").piece_on_square
test("45. Knight on e4 pinned by rook e8 - has 0 legal moves", len(knight.valid_moves) == 0)
print()

# Test 46: Pinned piece along diagonal
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, Pawn('w'), "d2")
place_piece(board, King('b'), "a8")
place_piece(board, Bishop('b'), "a5")
compute_moves(board, history)
print_board(board)
pawn = board.board_get_square("d2").piece_on_square
test("46. Pawn on d2 pinned by bishop a5 - can't move", len(pawn.valid_moves) == 0)
print()

# Test 47: Piece pinned but can move along pin line
board, history = setup_empty_board()
place_piece(board, King('w'), "e1")
place_piece(board, Rook('w'), "e4")
place_piece(board, King('b'), "a8")
place_piece(board, Rook('b'), "e8")
compute_moves(board, history)
print_board(board)
rook = board.board_get_square("e4").piece_on_square
test("47. Rook on e4 pinned but can move along e-file", "e5" in rook.valid_moves and "e8" in rook.valid_moves)
test("48. Rook on e4 pinned - can't move off e-file", "d4" not in rook.valid_moves and "f4" not in rook.valid_moves)
print()
print()

# ============================================================
# SECTION 9: X-Ray Attacks
# ============================================================
print("\n  ================ SECTION 9: X-Ray & Tactics ================")

# Test 49: Queen behind rook on same file (x-ray concept)
board, history = setup_empty_board()
place_piece(board, King('w'), "a1")
place_piece(board, King('b'), "h8")
place_piece(board, Rook('w'), "e4")
place_piece(board, Queen('w'), "e1")
compute_moves(board, history)
print_board(board)
# Rook protects e-file, queen behind supports
rook = board.board_get_square("e4").piece_on_square
queen = board.board_get_square("e1").piece_on_square
test("49. X-ray: Rook on e4 controls up to e8", "e8" in rook.valid_moves)
print()

# Test 50: Knight fork - attacks multiple pieces simultaneously
board, history = setup_empty_board()
place_piece(board, King('w'), "a1")
place_piece(board, King('b'), "e8")
place_piece(board, Knight('w'), "d6")
place_piece(board, Rook('b'), "f7")
compute_moves(board, history)
print_board(board)
knight = board.board_get_square("d6").piece_on_square
test("50. Knight fork: d6 attacks both king e8 and rook f7", "e8" in knight.valid_moves and "f7" in knight.valid_moves)
print()
print()

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'='*50}")
print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
print(f"{'='*50}")

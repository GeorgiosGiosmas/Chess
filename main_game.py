"""
Game Module - Responsible for initializing the game.

Playing without the GUI - You can play the game from terminal
by utilising functions like human_play(), print_info(), examine()
and next_turn() and the global variables Board, what_happened and history.

Basic GUI - Use of the Chess engine alongside the GUI.

"""
from piece import *
from board import *
from gui import *

def human_plays(colour):
    """
    Function that is called when we don't use the GUI and want to get 
    the input from the user.
    """
    global board, what_happened, history
    NotValidMoveException = Exception()
    YouHaveToMoveTheKingException = Exception()

    while True:
        print_info()
        move = input("Give the move you want to do. For example b4e7 or a1a6: ")
        try:
            from_square = move[:2]
            to_square = move[2:]

            if(from_square[0] not in board.files or from_square[1] not in board.ranks or to_square[0] not in board.files or to_square[1] not in board.ranks):
                raise NotValidMoveException

            if(board.board_get_square(from_square).piece_on_square is None or board.board_get_square(from_square).piece_on_square.colour != colour):
                print("No valid piece on that square. Try again")
            else:
              if(board.make_move(from_square, to_square, history) == 0):
                    break

        except Exception as e:
            print(e)


def computer_plays():
    """ Computer plays - We will implement it later. """
    global board, what_happened, history

def Black_plays():
    """ When Black plays. """
    colour = 'b'
    human_plays(colour)
    what_happened = "Black Played"

def White_plays():
    """ When White plays. """
    colour = 'w'
    human_plays(colour)
    what_happened = "White Played"

def print_info():
    """ Prints the state of the board after every move, when the GUI is not used. """
    global board, what_happened, history

    if what_happened == "Black Played":
        print("The Black played: ", history[-1])
        if(board.white_king_check == True):
            print("Your King is in check you have to protect him!")
    if what_happened == "White Played":
        print("The White played: ", history[-1])
        if(board.black_king_check == True):
            print("Your King is in check you have to protect him!")

    board.print_board_state()

def initial():
    """ Initializes the board, when the GUI is not used. """
    global board, what_happened, history

    board.board_initialize_pieces()
    board.get_all_pieces_moves(history)
    board.filter_legal_moves(history)
    what_happened = "Black Played"
    next_turn()

def examine():
    """ Examines if we have Promotion, Check, CheckMate, or Draw, when the GUI is not used. """
    global board, what_happened, history
    NotAValidChoice = Exception()

    # Check if either one of the two Kings is in check. If so, add + to the last move
    if(board.black_king_check == True or board.white_king_check == True):
        history[-1] = history[-1] + "+"

    # Check for promotion
    for i in range(8):
        # Check for white promotion
        if(board.board[7][i].piece_on_square is not None and board.board[7][i].piece_on_square.__str__()[0] == "P"):
            while True:
                try:
                    new_piece = input("Select the piece you want to replace the Pawn with. You can choose 'R', 'N', 'B', 'Q': ")
                    match new_piece:
                        case 'R':
                            board.board[7][i].piece_on_square = Rook('w')
                        case 'N':
                            board.board[7][i].piece_on_square = Knight('w')
                        case 'B':
                            board.board[7][i].piece_on_square = Bishop('w')
                        case 'Q':
                            board.board[7][i].piece_on_square = Queen('w')
                        case _:
                            raise NotAValidChoice
                    break
                except Exception as e:
                    print(e + " - Try Again!")
                
        # Check for black promotion
        elif(board.board[0][i].piece_on_square is not None and board.board[0][i].piece_on_square.__str__()[0] == "P"):
            while True:
                try:
                    new_piece = input("Select the piece you want to replace the Pawn with. You can choose 'R', 'N', 'B', 'Q': ")
                    match new_piece:
                        case 'R':
                            board.board[0][i].piece_on_square = Rook('b')
                        case 'N':
                            board.board[0][i].piece_on_square = Knight('b')
                        case 'B':
                            board.board[0][i].piece_on_square = Bishop('b')
                        case 'Q':
                            board.board[0][i].piece_on_square = Queen('b')
                        case _:
                            raise NotAValidChoice
                    break
                except Exception as e:
                    print(e + " - Try Again!")
        
    # Check for Checkmate or Draw for the White King
    if(not board.white_has_moves()):
        if(board.white_king_check == True):
            board.white_king_checkmate = True
            what_happened = "Black Won"
            history[-1] = history[-1] + "#"
        else:
            board.draw = True
            what_happened = "Draw"

    # Check for Checkmate or Draw for the Black King
    if(not board.black_has_moves()):
        if(board.black_king_check == True):
            board.black_king_checkmate = True
            what_happened = "White Won"
            history[-1] = history[-1] + "#"
        else:
            board.draw = True
            what_happened = "Draw"

def next_turn():
    """ Alternates the playing sequence between black and white, when the GUI is not used. """
    global what_happened, board, history
    
    while True:
        if what_happened == "Game Starts":
            print("The game starts. The white play first.")
            initial()
        elif what_happened == "White Played":
            board.get_all_pieces_moves(history)
            board.filter_legal_moves(history)
            examine()
            print(" ------------ Black Plays ------------ ")
            Black_plays()
        elif what_happened == "Black Played":
            board.get_all_pieces_moves(history)
            board.filter_legal_moves(history)
            examine()
            print(" ------------ White Plays ------------ ")
            White_plays()
        elif what_happened == "Draw":
            print(" ---- The game ended with a draw ---- ")
            play_again = input("Do you want to play again? (y/n): ")
            if(play_again == 'y'):
                board.reset()
                what_happened = "Game Starts"
            else:
                print("Thank you for playing! :-)")
                exit()
            
            board.reset()
        elif what_happened == "White Won":
            print(" ---- The white won with a checkmate ---- ")
            play_again = input("Do you want to play again? (y/n): ")
            if(play_again == 'y'):
                board.reset()
                what_happened = "Game Starts"
            else:
                print("Thank you for playing! :-)")
                exit()
        elif what_happened == "Black Won":
            print(" ---- The black won with a checkmate ---- ")
            play_again = input("Do you want to play again? (y/n): ")
            if(play_again == 'y'):
                board.reset()
                what_happened = "Game Starts"
            else:
                print("Thank you for playing! :-)")
                exit()

if __name__ == "__main__":
    root = tk.Tk()
    board = Board()
    game = ChessGameGUI(root, board)
    what_happened = "Game Starts"
    history = []
    root.mainloop()
    
from piece import *
from board import *

# Human plays
def human_plays(colour):
    global board, what_happened, history
    NotValidMoveException = Exception()

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
                if(board.make_move(from_square, to_square) == 0):

                    history.append()
                    break

        except Exception as e:
            print(e)


# Computer plays - We will implement it later
def computer_plays():
    global board, what_happened, history

# When Black plays
def Black_plays():
    colour = 'b'
    human_plays(colour)
    what_happened = "Black Played"

# When White plays
def White_plays():
    colour = 'w'
    human_plays(colour)
    what_happened = "White Played"

# Prints the state of the board after every move
def print_info():
    global board, what_happened, history

    if what_happened == "Black Played":
        print("The Black played: ", history[-1])
    if what_happened == "White Played":
        print("The White played: ", history[-1])

    board.print_board_state()


# Initializes the board
def initial():
    global board, what_happened, history

    board.board_initialize_pieces()
    what_happened = "Black Played"
    next_turn()

# Examines if we have a Check, CheckMate, or Draw
def examine():
    global board, what_happened, history

# Alternates the playing sequence between black and white
def next_turn():
    global what_happened, board
    
    while True:
        if what_happened == "Game Starts":
            print("The game starts. The white play first.")
            initial()
        elif what_happened == "White Played":
            board.get_all_pieces_moves()
            examine()
            print(" ------------ Black Plays ------------ ")
            Black_plays()
        elif what_happened == "Black Played":
            board.get_all_pieces_moves()
            examine()
            print(" ------------ White Plays ------------ ")
            White_plays()

if __name__ == "__main__":
    board = Board()
    what_happened = "Game Starts"
    history = []
    

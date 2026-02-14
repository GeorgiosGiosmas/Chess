from piece import *
from board import *


# When Black plays
def Black_plays():
    global board, what_happened, history


# When White plays
def White_plays():
    global board, what_happened, history

# Prints the state of the board after every move
def print_info():
    global board, what_happened, history


# Initializes the board
def initial():
    global board, what_happened, history

# Alternates the playing sequence between black and white
def next_turn():
    global what_happened

# Examines if we have a Check, CheckMate, or Draw
def examine():
    global board, what_happened, history

if __name__ == "__main__":
    pass

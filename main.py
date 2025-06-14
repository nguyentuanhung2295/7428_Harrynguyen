import streamlit as st
import numpy as np

# Initialize game board
BOARD_SIZE = 10
WIN_LENGTH = 5

if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.turn = "X"
    st.session_state.winner = None

def check_win(board, player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (
                check_line(board, row, col, 1, 0, player) or  # horizontal
                check_line(board, row, col, 0, 1, player) or  # vertical
                check_line(board, row, col, 1, 1, player) or  # diagonal down-right
                check_line(board, row, col, 1, -1, player)    # diagonal down-left
            ):
                return True
    return False

def check_line(board, row, col, delta_row, delta_col, player):
    count = 0
    for i in range(WIN_LENGTH):
        r = row + delta_row * i
        c = col + delta_col * i
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            count += 1
        else:
            break
    return count == WIN_LENGTH

def reset_game():
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.turn = "X"
    st.session_state.winner = None

# Title and reset button
st.title("🎮 Caro (Gomoku) Game")
if st.button("🔄 Reset Game"):
    reset_game()

# Game status
if st.session_state.winner:
    st.success(f"🎉 Player {st.session_state.winner} wins!")
else:
    st.info(f"🧑 Player {st.session_state.turn}'s turn")

# Draw game board
for row in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for col in range(BOARD_SIZE):
        cell = st.session_state.board[row][col]
        if cell:
            cols[col].markdown(f"### {cell}")
        elif not st.session_state.winner:
            if cols[col].button(" ", key=f"{row}-{col}"):
                st.session_state.board[row][col] = st.session_state.turn
                if check_win(st.session_state.board, st.session_state.turn):
                    st.session_state.winner = st.session_state.turn
                else:
                    st.session_state.turn = "O" if st.session_state.turn == "X" else "X"
                st.experimental_rerun()  # Refresh board immediately after a move

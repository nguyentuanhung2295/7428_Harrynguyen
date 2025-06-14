import streamlit as st
import random

BOARD_SIZE = 10
WIN_LENGTH = 5

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.winner = None
    st.session_state.turn = "X"  # Human always starts

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

def check_win(board, player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (
                check_line(board, row, col, 1, 0, player) or
                check_line(board, row, col, 0, 1, player) or
                check_line(board, row, col, 1, 1, player) or
                check_line(board, row, col, 1, -1, player)
            ):
                return True
    return False

def reset_game():
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.turn = "X"
    st.session_state.winner = None

def ai_move():
    # Very basic AI: choose a random empty cell
    empty_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if st.session_state.board[r][c] == ""]
    if empty_cells:
        row, col = random.choice(empty_cells)
        st.session_state.board[row][col] = "O"
        if check_win(st.session_state.board, "O"):
            st.session_state.winner = "O"

# UI
st.set_page_config(page_title="Caro vs AI")
st.title("🤖 Caro Game - Play vs AI")

if st.button("🔄 Reset Game"):
    reset_game()

if st.session_state.winner:
    st.success(f"🎉 Player {st.session_state.winner} wins!")
else:
    st.info(f"🧑 Your turn (X)")

# Game Board
for row in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for col in range(BOARD_SIZE):
        cell = st.session_state.board[row][col]
        if cell:
            cols[col].markdown(f"### {cell}")
        elif st.session_state.turn == "X" and not st.session_state.winner:
            if cols[col].button(" ", key=f"{row}-{col}"):
                st.session_state.board[row][col] = "X"
                if check_win(st.session_state.board, "X"):
                    st.session_state.winner = "X"
                else:
                    st.session_state.turn = "O"
                    ai_move()
                    if not st.session_state.winner:
                        st.session_state.turn = "X"
                st.rerun()

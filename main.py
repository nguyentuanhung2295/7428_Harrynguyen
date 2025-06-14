import streamlit as st
import random

BOARD_SIZE = 10
WIN_LENGTH = 5

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.winner = None
    st.session_state.turn = "X"

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

def simulate_move(board, row, col, player):
    board[row][col] = player
    win = check_win(board, player)
    board[row][col] = ""
    return win

def get_smart_ai_move():
    empty_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if st.session_state.board[r][c] == ""]

    # 1. Try to win
    for r, c in empty_cells:
        if simulate_move(st.session_state.board, r, c, "O"):
            return r, c

    # 2. Block player from winning
    for r, c in empty_cells:
        if simulate_move(st.session_state.board, r, c, "X"):
            return r, c

    # 3. Try to play near the center or near other pieces
    center = BOARD_SIZE // 2
    empty_cells.sort(key=lambda x: abs(x[0] - center) + abs(x[1] - center))
    return empty_cells[0] if empty_cells else None

def ai_move():
    move = get_smart_ai_move()
    if move:
        r, c = move
        st.session_state.board[r][c] = "O"
        if check_win(st.session_state.board, "O"):
            st.session_state.winner = "O"

# UI
st.set_page_config(page_title="Caro AI")
st.title("🤖 Caro Game - Smarter AI")

if st.button("🔄 Reset Game"):
    reset_game()

if st.session_state.winner:
    st.success(f"🎉 Player {st.session_state.winner} wins!")
else:
    st.info(f"🧑 Your turn (X)")

# Draw the board
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

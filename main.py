import streamlit as st
import random

ROWS, COLS = 6, 6
ITEMS = {
    "💰": 100,  # Gold
    "🪨": 20,   # Rock
    "💎": 250,  # Diamond
    "": 0       # Empty
}

if "map" not in st.session_state:
    st.session_state.map = [[random.choices(["💰", "🪨", "💎", ""], [0.2, 0.3, 0.1, 0.4])[0] for _ in range(COLS)] for _ in range(ROWS)]
    st.session_state.revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    st.session_state.score = 0
    st.session_state.turns_left = 10

def reset_game():
    st.session_state.map = [[random.choices(["💰", "🪨", "💎", ""], [0.2, 0.3, 0.1, 0.4])[0] for _ in range(COLS)] for _ in range(ROWS)]
    st.session_state.revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    st.session_state.score = 0
    st.session_state.turns_left = 10

st.set_page_config(page_title="🎣 Game Đào Vàng")
st.title("🎣 Game Đào Vàng")

st.markdown(f"**Điểm của bạn:** {st.session_state.score} | **Lượt còn lại:** {st.session_state.turns_left}")

if st.button("🔄 Chơi lại"):
    reset_game()

# Game Board
for row in range(ROWS):
    cols = st.columns(COLS)
    for col in range(COLS):
        if st.session_state.revealed[row][col]:
            icon = st.session_state.map[row][col] or "⬛"
        else:
            icon = "❓"

        if cols[col].button(icon, key=f"{row}-{col}") and not st.session_state.revealed[row][col] and st.session_state.turns_left > 0:
            st.session_state.revealed[row][col] = True
            item = st.session_state.map[row][col]
            st.session_state.score += ITEMS[item]
            st.session_state.turns_left -= 1
            st.rerun()

# Kết thúc game
if st.session_state.turns_left == 0:
    st.markdown("---")
    st.success(f"🎉 Game kết thúc! Tổng điểm của bạn là **{st.session_state.score}**.")
    if st.session_state.score >= 500:
        st.balloons()
        st.markdown("🥳 Bạn đã vượt qua mục tiêu!")
    else:
        st.markdown("😢 Hãy thử lại để đạt điểm cao hơn!")

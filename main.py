import streamlit as st
import time
import random

# Game Constants
ROWS, COLS = 6, 9
ITEMS = {
    "💰": 100,  # Gold
    "🪨": 30,   # Rock
    "💎": 250,  # Diamond
    "": 0       # Empty
}
SWING_ANGLES = ["|", "\\", "/", "|", "/"]
ANGLE_OFFSETS = [0, 1, -1, 0, 1]
INITIAL_MOVES = 10
QUOTA = 400

# Session Initialization
if "grid" not in st.session_state:
    def reset_game():
        st.session_state.grid = [
            [random.choices(["💰", "🪨", "💎", ""], [0.2, 0.3, 0.1, 0.4])[0] for _ in range(COLS)]
            for _ in range(ROWS)
        ]
        st.session_state.score = 0
        st.session_state.angle_idx = 0
        st.session_state.running = True
        st.session_state.message = ""
        st.session_state.moves_left = INITIAL_MOVES
        st.session_state.upgrades = {"speed": 1, "dynamite": 0}
        st.session_state.swing_counter = 0
        st.session_state.game_over = False

    reset_game()

# Game Functions
def render_game():
    st.markdown(f"### 🧍 Người chơi")
    line = ["⬛"] * COLS
    center = COLS // 2 + ANGLE_OFFSETS[st.session_state.angle_idx]
    line[center] = SWING_ANGLES[st.session_state.angle_idx]
    st.markdown("".join(line))

    st.markdown("---")
    for row in st.session_state.grid:
        st.markdown("".join(cell or "⬜" for cell in row))
    st.markdown("---")

    st.markdown(f"**💎 Điểm hiện tại:** `{st.session_state.score}` | 🎯 Mục tiêu: `{QUOTA}` | 🔄 Lượt còn: `{st.session_state.moves_left}`")
    if st.session_state.message:
        st.success(st.session_state.message)

def drop_hook():
    col = COLS // 2 + ANGLE_OFFSETS[st.session_state.angle_idx]
    for row in range(ROWS):
        item = st.session_state.grid[row][col]
        time.sleep(0.05 / st.session_state.upgrades["speed"])
        if item:
            st.session_state.score += ITEMS[item]
            st.session_state.grid[row][col] = ""
            st.session_state.message = f"🎯 Trúng {item}! +{ITEMS[item]} điểm!"
            break
    else:
        st.session_state.message = "😢 Không trúng gì cả!"
    st.session_state.moves_left -= 1
    if st.session_state.moves_left == 0:
        st.session_state.running = False
        st.session_state.game_over = True

def show_shop():
    st.sidebar.markdown("## 🛍️ Cửa hàng")
    if st.sidebar.button("⚡ Tăng tốc móc (50 điểm)") and st.session_state.score >= 50:
        st.session_state.upgrades["speed"] += 0.5
        st.session_state.score -= 50
    if st.sidebar.button("💣 Mua thuốc nổ (30 điểm)") and st.session_state.score >= 30:
        st.session_state.upgrades["dynamite"] += 1
        st.session_state.score -= 30

# Main App
st.set_page_config(page_title="🎣 Đào Vàng Hoàn Chỉnh")
st.title("🎮 Game Đào Vàng - Phiên bản Hoàn Chỉnh")

c1, c2 = st.columns(2)
with c1:
    if st.button("🎣 Thả Móc", disabled=not st.session_state.running):
        drop_hook()
with c2:
    if st.button("🔄 Chơi lại"):
        reset_game()

render_game()

if st.session_state.running:
    st.session_state.swing_counter += 1
    if st.session_state.swing_counter % 3 == 0:
        st.session_state.angle_idx = (st.session_state.angle_idx + 1) % len(SWING_ANGLES)
    time.sleep(0.3)
    st.rerun()

if st.session_state.game_over:
    st.markdown("---")
    if st.session_state.score >= QUOTA:
        st.balloons()
        st.success(f"🎉 Bạn đã thắng! Tổng điểm: {st.session_state.score}")
        show_shop()
    else:
        st.error(f"😢 Thua cuộc. Tổng điểm: {st.session_state.score}. Hãy thử lại!")

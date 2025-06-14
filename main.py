import streamlit as st
import numpy as np

# Game Settings
GRID_SIZE = 10
FIRE_ICON = "🔴"
SNOW_ICON = "🔵"
WATER = "🌊"
LAVA = "🔥"
GOAL = "🏁"
EMPTY = "⬜"

# Initialize session state
if "fire_pos" not in st.session_state:
    st.session_state.fire_pos = [0, 0]
    st.session_state.snow_pos = [GRID_SIZE - 1, GRID_SIZE - 1]
    st.session_state.goal = [GRID_SIZE // 2, GRID_SIZE // 2]
    st.session_state.turn = "Fire"
    st.session_state.win = False

# Obstacles map
obstacles = np.full((GRID_SIZE, GRID_SIZE), "")
obstacles[2][3] = WATER
obstacles[3][3] = WATER
obstacles[6][4] = LAVA
obstacles[5][5] = LAVA

def is_valid(pos, player):
    r, c = pos
    if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
        return False
    cell = obstacles[r][c]
    if player == "Fire" and cell == WATER:
        return False
    if player == "Snow" and cell == LAVA:
        return False
    return True

def move_player(direction):
    if st.session_state.win:
        return
    delta = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }[direction]

    player = st.session_state.turn
    pos = st.session_state.fire_pos if player == "Fire" else st.session_state.snow_pos
    new_pos = [pos[0] + delta[0], pos[1] + delta[1]]

    if is_valid(new_pos, player):
        if player == "Fire":
            st.session_state.fire_pos = new_pos
            st.session_state.turn = "Snow"
        else:
            st.session_state.snow_pos = new_pos
            st.session_state.turn = "Fire"

    # Check win
    if (st.session_state.fire_pos == st.session_state.goal and
        st.session_state.snow_pos == st.session_state.goal):
        st.session_state.win = True

def render_grid():
    for r in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for c in range(GRID_SIZE):
            icon = EMPTY
            if [r, c] == st.session_state.fire_pos:
                icon = FIRE_ICON
            elif [r, c] == st.session_state.snow_pos:
                icon = SNOW_ICON
            elif [r, c] == st.session_state.goal:
                icon = GOAL
            elif obstacles[r][c] == WATER:
                icon = WATER
            elif obstacles[r][c] == LAVA:
                icon = LAVA
            cols[c].markdown(icon)

# Title & instructions
st.set_page_config(page_title="Fire & Snow")
st.title("🔥❄️ Fire and Snow")
st.markdown("Take turns moving **Fire (🔴)** and **Snow (🔵)** to the goal (🏁). Avoid water or fire depending on the character.")

if st.button("🔄 Reset Game"):
    st.session_state.fire_pos = [0, 0]
    st.session_state.snow_pos = [GRID_SIZE - 1, GRID_SIZE - 1]
    st.session_state.turn = "Fire"
    st.session_state.win = False

# Render the grid
render_grid()

# Controls
st.markdown(f"**{st.session_state.turn}'s turn**")
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬆️"):
        move_player("up")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️"):
        move_player("left")
with col2:
    if st.button("⬇️"):
        move_player("down")
with col3:
    if st.button("➡️"):
        move_player("right")

# Win check
if st.session_state.win:
    st.success("🎉 Both players reached the goal! You win!")

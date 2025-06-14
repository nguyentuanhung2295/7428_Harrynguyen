import streamlit as st

# ---- Simulated Database ----
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123"}  # Preloaded admin user

# ---- Session Management ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ---- Login Functionality ----
def login_form():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Invalid username or password.")

# ---- Register Functionality ----
def register_form():
    st.subheader("📝 Register")
    new_user = st.text_input("Choose a username")
    new_pass = st.text_input("Choose a password", type="password")
    confirm_pass = st.text_input("Confirm password", type="password")

    if st.button("Register"):
        if new_user in st.session_state.users:
            st.warning("Username already exists.")
        elif new_pass != confirm_pass:
            st.warning("Passwords do not match.")
        elif not new_user or not new_pass:
            st.warning("Please fill in all fields.")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("Registration successful! You can now login.")

# ---- Main Interface ----
st.set_page_config(page_title="Login System")

st.title("🛋️ Furniture App - Login/Register")

if not st.session_state.logged_in:
    form_type = st.radio("Choose an option", ["Login", "Register"], horizontal=True)

    if form_type == "Login":
        login_form()
    else:
        register_form()
else:
    st.success(f"You are logged in as **{st.session_state.username}**.")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

    # Simulated protected content
    st.markdown("### 🪑 Welcome to the Furniture Store Dashboard!")
    st.markdown("- Browse products\n- Add to cart\n- Check out")


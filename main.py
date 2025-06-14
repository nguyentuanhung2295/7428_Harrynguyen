import streamlit as st

# Sample data
furniture_data = [
    {
        "name": "Modern Chair",
        "category": "Chair",
        "price": 120,
        "image": "https://images.unsplash.com/photo-1578898887238-5165e9861606",
        "description": "Comfortable modern chair with wooden legs."
    },
    {
        "name": "Wooden Table",
        "category": "Table",
        "price": 250,
        "image": "https://images.unsplash.com/photo-1598300051453-695f3e6f1a4c",
        "description": "Stylish wooden dining table, seats 6."
    },
    {
        "name": "Luxury Sofa",
        "category": "Sofa",
        "price": 450,
        "image": "https://images.unsplash.com/photo-1585559600435-6ba47b6dddf4",
        "description": "Spacious 3-seat leather sofa with plush cushions."
    }
]

st.set_page_config(page_title="Furniture Store", layout="wide")

st.title("🛋️ Furniture Shop")
st.markdown("Welcome to our online store. Browse and add your favorite furniture.")

# Sidebar filters
categories = list(set(item['category'] for item in furniture_data))
selected_category = st.sidebar.selectbox("Filter by Category", ["All"] + categories)

# Cart session
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Display products
cols = st.columns(3)

for idx, item in enumerate(furniture_data):
    if selected_category != "All" and item["category"] != selected_category:
        continue

    with cols[idx % 3]:
        st.image(item['image'], width=250)
        st.subheader(item['name'])
        st.write(item['description'])
        st.write(f"💲Price: ${item['price']}")
        if st.button(f"Add to Cart - {item['name']}", key=item['name']):
            st.session_state.cart.append(item)
            st.success(f"{item['name']} added to cart!")

# Show cart
st.sidebar.markdown("## 🛒 Your Cart")
if st.session_state.cart:
    total = 0
    for item in st.session_state.cart:
        st.sidebar.write(f"- {item['name']} (${item['price']})")
        total += item['price']
    st.sidebar.markdown(f"**Total: ${total}**")
else:
    st.sidebar.write("Your cart is empty.")

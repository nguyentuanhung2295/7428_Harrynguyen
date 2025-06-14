import streamlit as st
import pandas as pd
import uuid

# Simulate a database
if 'products' not in st.session_state:
    st.session_state.products = pd.DataFrame([
        {"id": str(uuid.uuid4()), "name": "Modern Chair", "category": "Chair", "price": 120,
         "image": "https://images.unsplash.com/photo-1578898887238-5165e9861606",
         "description": "Comfortable modern chair with wooden legs."},
        {"id": str(uuid.uuid4()), "name": "Wooden Table", "category": "Table", "price": 250,
         "image": "https://images.unsplash.com/photo-1598300051453-695f3e6f1a4c",
         "description": "Stylish wooden dining table, seats 6."},
        {"id": str(uuid.uuid4()), "name": "Luxury Sofa", "category": "Sofa", "price": 450,
         "image": "https://images.unsplash.com/photo-1585559600435-6ba47b6dddf4",
         "description": "Spacious 3-seat leather sofa with plush cushions."}
    ])

if 'cart' not in st.session_state:
    st.session_state.cart = []

st.set_page_config(page_title="🛋️ Furniture Store", layout="wide")
st.title("🛍️ Welcome to Our Furniture Shop")
st.markdown("Browse our collection and manage your cart. Admins can add new products.")

# Sidebar navigation
menu = st.sidebar.radio("Menu", ["Home", "Cart", "Admin"])

# Filter categories
def filter_products():
    categories = ["All"] + sorted(st.session_state.products['category'].unique().tolist())
    selected = st.sidebar.selectbox("Filter by Category", categories)
    if selected == "All":
        return st.session_state.products
    else:
        return st.session_state.products[st.session_state.products['category'] == selected]

# Home page
if menu == "Home":
    filtered = filter_products()
    cols = st.columns(3)
    for i, (_, item) in enumerate(filtered.iterrows()):
        with cols[i % 3]:
            st.image(item['image'], width=250)
            st.subheader(item['name'])
            st.caption(item['description'])
            st.write(f"💲 **{item['price']} USD**")
            if st.button("Add to Cart", key=item['id']):
                st.session_state.cart.append(item.to_dict())
                st.success(f"✅ {item['name']} added to cart!")

# Cart page
elif menu == "Cart":
    st.subheader("🛒 Your Shopping Cart")
    if st.session_state.cart:
        cart_df = pd.DataFrame(st.session_state.cart)
        total = cart_df['price'].sum()
        st.table(cart_df[['name', 'price']])
        st.markdown(f"### 💰 Total: **${total}**")
        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.success("Cart cleared!")
    else:
        st.info("Your cart is empty.")

# Admin page
elif menu == "Admin":
    st.subheader("🔧 Admin Panel: Add New Product")
    with st.form("add_form"):
        name = st.text_input("Product Name")
        category = st.text_input("Category")
        price = st.number_input("Price (USD)", min_value=1)
        image = st.text_input("Image URL")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Add Product")
        if submitted:
            new_product = {
                "id": str(uuid.uuid4()),
                "name": name,
                "category": category,
                "price": price,
                "image": image,
                "description": description
            }
            st.session_state.products = pd.concat([
                st.session_state.products,
                pd.DataFrame([new_product])
            ], ignore_index=True)
            st.success(f"✅ Product '{name}' added!")

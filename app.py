import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# --- File paths ---
EXPENSE_FILE = "expenses.json"
USER_FILE = "users.json"

# --- Helper functions ---
def load_data():
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(EXPENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# --- Streamlit UI ---
st.set_page_config(page_title="💰 Expense Tracker", layout="wide")

st.markdown("""
    <h1 style="text-align:center; color:#00B4D8;">💰 Expense Tracker</h1>
    <p style="text-align:center;">Track your spending with ease!</p>
""", unsafe_allow_html=True)

users = load_users()
data = load_data()

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Sign Up":
    st.subheader("Create New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if username in users:
            st.warning("Username already exists.")
        else:
            users[username] = password
            save_users(users)
            st.success("Account created successfully! You can now log in.")

elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.success(f"Welcome, {username}!")
            st.session_state["user"] = username
        else:
            st.error("Invalid username or password")

# --- Logged-in User Interface ---
if "user" in st.session_state:
    st.sidebar.title(f"Hello, {st.session_state['user']} 👋")

    tabs = st.tabs(["➕ Add Expense", "📊 View Summary", "📈 Analytics"])

    # Add Expense Tab
    with tabs[0]:
        st.header("Add Expense")
        category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
        amount = st.number_input("Amount", min_value=1.0)
        date = st.date_input("Date")
        note = st.text_input("Note (optional)")
        if st.button("Add Expense"):
            user_expenses = data.get(st.session_state["user"], [])
            user_expenses.append({"category": category, "amount": amount, "date": str(date), "note": note})
            data[st.session_state["user"]] = user_expenses
            save_data(data)
            st.success("Expense added successfully!")

    # View Summary Tab
    with tabs[1]:
        st.header("View Summary")
        user_expenses = data.get(st.session_state["user"], [])
        if user_expenses:
            df = pd.DataFrame(user_expenses)
            st.dataframe(df)
            total = df["amount"].sum()
            st.write(f"### 💵 Total Expenses: ₹{total}")
        else:
            st.info("No expenses yet. Add some above!")

    # Analytics Tab
    with tabs[2]:
        st.header("Expense Analytics")
        user_expenses = data.get(st.session_state["user"], [])
        if user_expenses:
            df = pd.DataFrame(user_expenses)
            fig = px.pie(df, names="category", values="amount", title="Expenses by Category", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data to show.")

from vars import *
import streamlit as st

if "accounts" not in st.session_state:
    st.session_state.accounts = {}

# ------------------------------
# Load existing accounts
# ------------------------------
load_all_accounts()

st.title("🏦 Welcome to the Bank!!!")

choice = st.radio("Choose an option:", ["Register", "Login"])
user = None

# ------------------------------
# Registration or Login
# ------------------------------
if choice == "Register":
    register()
elif choice == "Login":
    user = login()
    if user:
        st.success(f"Welcome back, {user.owner}!")
        st.info(f"Your current balance is: ${user.balance}")

# ------------------------------
# Banking options if logged in
# ------------------------------
if st.session_state.current_user:
    user = st.session_state.accounts[st.session_state.current_user]

    st.subheader("Banking Options")
    option = st.radio("Select what you would like to do:", ["Withdraw", "Deposit", "Check Balance"])

    if option == "Withdraw":
        amount = st.number_input("Enter amount to withdraw:", min_value=1.0, step=1.0)
        if st.button("Withdraw"):
            user.withdraw(amount)

    elif option == "Deposit":
        user.deposit()

    elif option == "Check Balance":
        user.check_balance()

    st.divider()
    logout()

else:
    st.warning("Please log in to access banking options.")

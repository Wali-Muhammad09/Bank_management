from vars import *
import streamlit as st
import pandas as pd
import uuid

# ---------------------------------------
# Generate unique session ID per user
# ---------------------------------------
def get_session_id():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

session_id = get_session_id()

# ---------------------------------------
# Load existing accounts
# ---------------------------------------
load_all_accounts()

# Prepare sidebar account table
acc_price = []
for account in accounts:
    acc_price.append(accounts[account].balance)
def leaderboard():
    acc_price = []
    for account in accounts:
        acc_price.append(accounts[account].balance)

    data = {"Name": list(accounts.keys()), "Balance": acc_price}
    df = pd.DataFrame(data)

    df = df.sort_values(by="Balance", ascending=False).reset_index(drop=True)

    
st.sidebar.header("🏆 Leaderboard (Top Accounts)")
    st.sidebar.dataframe(df)

leaderboard()
# ---------------------------------------

st.title("🏦 Welcome to the Bank!!!")

choice = st.radio("Choose an option:", ["Register", "Login"])
user = None

# ------------------------------
# Registration or Login
# ------------------------------
if choice == "Register":
    register()
elif choice == "Login":
    user = login(session_id)
    if user:
        st.success(f"Welcome back, {user.owner}!")
        st.info(f"Your current balance is: ${user.balance}")

# ------------------------------
# Banking options if logged in
# ------------------------------
if session_id in sessions:
    current_user = sessions[session_id]
    user = accounts[current_user]

    st.subheader("Banking Options")
    option = st.radio("Select what you would like to do:", ["Make a transaction", "Deposit", "Check Balance"])

    if option == "Make a transaction":
        amount = st.number_input("Enter amount to send:", min_value=1.0, step=1.0)
        target_name = st.selectbox(
            "Choose who you want to send money to:",
            [acc.owner for acc in accounts.values() if acc.owner != user.owner]
        )

        if st.button("Send"):
            if target_name not in accounts:
                st.warning("That account does not exist!\nMake sure to enter the right name")
            else:
                user.transaction(amount, accounts[target_name])
                leaderboard()

    elif option == "Deposit":
        user.deposit()

    elif option == "Check Balance":
        user.check_balance()

    st.divider()
    logout(session_id)
    leaderboard()
else:
    st.warning("Please log in to access banking options.")



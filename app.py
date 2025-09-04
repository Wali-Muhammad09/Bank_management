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

# ---------------------------------------
# Leaderboard function
# ---------------------------------------
def leaderboard():
    acc_price = [accounts[account].balance for account in accounts]

    data = {"Name": list(accounts.keys()), "Balance": acc_price}
    df = pd.DataFrame(data)

    # Sort balances from highest to lowest
    df = df.sort_values(by="Balance", ascending=False).reset_index(drop=True)

    st.sidebar.header("🏆 Leaderboard (Top Accounts)")
    st.sidebar.dataframe(df)

# Always show leaderboard
leaderboard()

# ---------------------------------------
# Main app
# ---------------------------------------
st.title("🏦 Welcome


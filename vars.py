import streamlit as st
import json
import glob

# ------------------------------
# Redemption codes
#      Codes|Rewards(dollars)
codes_dict={"13902": 100
     , "87362": 1000
     , "99101": 10000
     , "86368": 100000}

# ------------------------------
# CLASSES
# ------------------------------
class BankAccount:
    def __init__(self, owner, password, balance=0):
        self.owner = owner
        self.pw = password
        self.balance = balance

    def deposit(self):
        code = st.text_input("Enter a Code to Redeem")
        if st.button("Redeem"):
            if code:
                if code in codes_dict:
                    self.balance += codes_dict[code]
                    st.text(f"${codes_dict[code]}   deposited. New balance: ${self.balance}")
                else:
                    st.error("That code does not exist")
        save_all_accounts()

    def withdraw(self, amount):
        if amount > self.balance:
            st.text("Insufficient funds.")
        else:
            self.balance -= amount
            st.text(f"${amount} withdrawn. New balance: ${self.balance}")
            save_all_accounts()

    def check_balance(self):
        st.text(f"Account balance: ${self.balance}")
        save_all_accounts()


# ------------------------------
# INITIAL STATE
# ------------------------------
if "accounts" not in st.session_state:
    st.session_state.accounts = {}

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# ------------------------------
# FUNCTIONS
# ------------------------------
def register():
    name = st.text_input("Enter your name:")
    password = st.text_input("Create a password:", type="password")
    if st.button("Register"):
        if name in st.session_state.accounts:
            st.warning("Account already exists!")
        else:
            st.session_state.accounts[name] = BankAccount(name, password)
            st.success(f"Account created for {name}!")
            save_all_accounts()


def login():
    name = st.text_input("Enter your name:")
    password = st.text_input("Enter your password:", type="password")
    if st.button("Login"):
        user = st.session_state.accounts.get(name)
        if user and user.pw == password:
            st.session_state.current_user = name
            st.success(f"Logged in as {name}!")
        else:
            st.error("Invalid name or password!")

    # Return the currently logged-in user object if available
    if st.session_state.current_user:
        return st.session_state.accounts[st.session_state.current_user]
    return None


def logout():
    if st.button("Logout"):
        st.session_state.current_user = None
        st.success("Logged out successfully!")


def save_all_accounts():
    for user in st.session_state.accounts.values():
        data = {
            "owner": user.owner,
            "password": user.pw,
            "balance": int(user.balance)
        }
        with open(f"{user.owner}.json", "w") as f:
            json.dump(data, f, indent=4)


def load_all_accounts():
    for file in glob.glob("*.json"):
        with open(file, "r") as f:
            data = json.load(f)
        st.session_state.accounts[data["owner"]] = BankAccount(
            data["owner"], data["password"], data["balance"]
        )

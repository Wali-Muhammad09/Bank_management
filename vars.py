import streamlit as st
import json
import glob
import pandas as pd

# Global state (instead of session_state)
accounts = {}
current_user = None
acc = []

# ------------------------------
# Redemption codes
# ------------------------------
codes_dict = {
    "13902": 100,
    "87362": 1000,
    "99101": 10000,
    "86368": 100000,
}

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
                    st.text(f"${codes_dict[code]} deposited. New balance: ${self.balance}")
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
# FUNCTIONS
# ------------------------------
def register():
    global accounts
    name = st.text_input("Enter your name:")
    password = st.text_input("Create a password:", type="password")
    if st.button("Register"):
        if name in accounts:
            st.warning("Account already exists!")
        else:
            accounts[name] = BankAccount(name, password)
            st.success(f"Account created for {name}!")
            save_all_accounts()
    if name not in acc:
        acc.append(name)


def login():
    global accounts, current_user
    name = st.text_input("Enter your name:")
    password = st.text_input("Enter your password:", type="password")
    if st.button("Login"):
        user = accounts.get(name)
        if user and user.pw == password:
            current_user = name
            st.success(f"Logged in as {name}!")
        else:
            st.error("Invalid name or password!")

    if name not in acc:
        acc.append(name)

    # Return the currently logged-in user object if available
    if current_user:
        return accounts[current_user]
    return None


def logout():
    global current_user
    if st.button("Logout"):
        current_user = None
        st.success("Logged out successfully!")


def save_all_accounts():
    global accounts
    for user in accounts.values():
        data = {"owner": user.owner, "password": user.pw, "balance": int(user.balance)}
        with open(f"{user.owner}.json", "w") as f:
            json.dump(data, f, indent=4)


def load_all_accounts():
    global accounts
    for file in glob.glob("*.json"):
        with open(file, "r") as f:
            data = json.load(f)
        accounts[data["owner"]] = BankAccount(
            data["owner"], data["password"], data["balance"]
        )

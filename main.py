import streamlit as st
import random

# Backend logic
class BankAccount:
    def __init__(self, cnic, name, balance):
        self.cnic = cnic
        self.name = name
        self.__balance = balance
        self.account_number = random.randint(1000, 9999)
        self.__pin = random.randint(1000, 9999)

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            return False
        self.__balance -= amount
        return True

    def transfer(self, amount, beneficiary):
        if amount > self.__balance:
            return False
        self.__balance -= amount
        beneficiary.__balance += amount
        return True

    def get_balance(self):
        return self.__balance

    def get_pin(self):
        return self.__pin

    def convert_to_dict(self):
        return {
            "CNIC": self.cnic,
            "Name": self.name,
            "Account Number": self.account_number,
            "PIN": self.__pin,
            "Balance": self.__balance
        }


# Initialize the accounts list in session state
if "accounts" not in st.session_state:
    st.session_state.accounts = []


def find_account(acc_no, pin=None):
    for acc in st.session_state.accounts:
        if acc.account_number == acc_no:
            if pin is None or acc.get_pin() == pin:
                return acc
    return None

# Frontend Logic
st.set_page_config(page_title='Banking System', page_icon='🏦')
st.title("🏦 Simple Bank Management System")

menu = st.sidebar.selectbox(
    "Select Option",
    ["Create Account", "Deposit", "Withdraw", "Transfer", "Check Balance", "All Accounts"]
)

# Create Account
if menu == "Create Account":
    st.header("➕ Create Account")

    cnic = st.text_input("CNIC")
    name = st.text_input("Account Holder Name")
    deposit = st.number_input("Initial Deposit", min_value=0)

    if st.button("Create"):
        acc = BankAccount(cnic, name, deposit)
        st.session_state.accounts.append(acc)

        st.success("Account Created Successfully")
        st.write("Account Number:", acc.account_number)
        st.write("PIN:", acc.get_pin())

# Deposite Amount
elif menu == "Deposit":
    st.header("📥 Deposit Amount")

    acc_no = st.number_input("Account Number", min_value=1000, max_value=9999)
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        acc = find_account(acc_no)
        if acc:
            acc.deposit(amount)
            st.success(f"New Balance: Rs {acc.get_balance()}")
        else:
            st.error("Account Not Found")

# Withdraw Amount
elif menu == "Withdraw":
    st.header("📤 Withdraw Amount")
    acc_no = st.number_input("Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("PIN", min_value=1000, max_value=9999)
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        acc = find_account(acc_no, pin)
        if acc:
            if acc.withdraw(amount):
                st.success(f"Remaining Balance: Rs {acc.get_balance()}")
            else:
                st.error("Insufficient Balance")
        else:
            st.error("Invalid Account or PIN")

# Transfer Amount
elif menu == "Transfer":
    st.header("💸 Transfer Amount")

    sender_no = st.number_input("Your Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("PIN", min_value=1000, max_value=9999)
    amount = st.number_input("Amount", min_value=1)
    receiver_no = st.number_input("Beneficiary Account Number", min_value=1000, max_value=9999)

    if st.button("Transfer"):
        sender = find_account(sender_no, pin)
        receiver = find_account(receiver_no)

        if sender and receiver:
            if sender.transfer(amount, receiver):
                st.success(f"Transfer Successful! Remaining Balance: Rs {sender.get_balance()}")
            else:
                st.error("Insufficient Balance")
        else:
            st.error("Invalid Account or PIN")

# Check Balance
elif menu == "Check Balance":
    st.header("💰 Check Balance")

    acc_no = st.number_input("Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("PIN", min_value=1000, max_value=9999)

    if st.button("Check"):
        acc = find_account(acc_no, pin)
        if acc:
            st.success(f"Current Balance: Rs {acc.get_balance()}")
        else:
            st.error("Invalid Account or PIN")

# All Accounts
elif menu == "All Accounts":
    st.header("🏛️ All Accounts")
    data = []
    for acc in st.session_state.accounts:
        data.append(acc.convert_to_dict())
    st.table(data)
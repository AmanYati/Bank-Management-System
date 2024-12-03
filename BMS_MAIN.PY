import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

class Bank:

    
    def __init__(self):
        self.accounts = {}
        self.users = {"admin": "admin123"}
        self.logged_in_user = None
        self.db = mysql.connector.connect(
            host="localhost",  # Replace with your MySQL host if different
            user="root",  # Replace with your MySQL username
            password="admin123",  # Replace with your MySQL password
            database="BankDB"
        )
        self.cursor = self.db.cursor()


        

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            self.logged_in_user = username
            return True
        return False

    def create_account(self, bank_name, acc_num, name, acc_type, balance):
        try:
            print(bank_name)
            balance = float(balance)
            if acc_type not in ["Savings", "Current", "Fixed Deposit", "Student"]:
                return "Invalid account type."
            
            min_balance = {"Savings": 500, "Current": 1000, "Fixed Deposit": 5000, "Student": 0}[acc_type]
            if balance < min_balance:
                return f"Initial balance for {acc_type} account must be at least {min_balance}."
            
            if acc_num in self.accounts:
                return "Account number already exists."
            
            self.accounts[acc_num] = {'bank_name': bank_name, 'name': name, 'balance': balance, 'type': acc_type}
            self.cursor.execute("""  INSERT INTO ALL_ACCOUNTS (account_number, account_holder_name, balance, account_type, bank_name) VALUES (%s, %s, %s, %s, %s) """, (acc_num, name, balance, acc_type, bank_name))
            self.db.commit()
            return "Account created successfully."
        except ValueError:
            return "Invalid balance amount."
        

    def update_account(self, acc_num, new_name=None, new_balance=None, new_acc_type=None):
        try:
            if acc_num not in self.accounts:
                return "Account not found."

            if new_acc_type and new_acc_type not in ["Savings", "Current", "Fixed Deposit", "Student"]:
                return "Invalid account type."

            min_balance = {"Savings": 500, "Current": 1000, "Fixed Deposit": 5000, "Student": 0}[new_acc_type] if new_acc_type else None

            if new_balance:
                new_balance = float(new_balance)
                
                if new_balance < min_balance:
                    return f"Initial balance for {new_acc_type} account must be at least {min_balance}."
                self.accounts[acc_num]['balance'] = new_balance

            if new_name:
                self.accounts[acc_num]['name'] = new_name

            if new_acc_type:
                self.accounts[acc_num]['type'] = new_acc_type

            return "Account updated successfully."
        except ValueError:
            return "Invalid balance amount."

    def deposit(self, acc_num, amount):
        try:
            # Convert amount to float
            amount = float(amount)
            
            # Check if the account exists in the database
            self.cursor.execute("SELECT * FROM ALL_ACCOUNTS WHERE account_number = %s", (acc_num,))
            account = self.cursor.fetchone()

            if not account:
                return "Account not found."
            
            # Convert the current balance from Decimal to float
            current_balance = float(account[2])  # Assuming account[2] is the balance column

            # Calculate the new balance
            new_balance = current_balance + amount
            
            # Execute the update query to modify the balance
            self.cursor.execute("UPDATE ALL_ACCOUNTS SET balance = %s WHERE account_number = %s", (new_balance, acc_num))
            self.db.commit()
            
            # Check if any row was updated (balance updated)
            if self.cursor.rowcount > 0:
                return f"Deposited {amount} into account {acc_num}. New balance: {new_balance}"
            else:
                return "Deposit failed, no changes made."

        except ValueError:
            return "Invalid deposit amount."
        except mysql.connector.Error as err:
            return f"Error: {err}"


    def withdraw(self, acc_num, amount):
        try:
            # Convert the amount to float
            amount = float(amount)

            # Check if the account exists in the database
            self.cursor.execute("SELECT * FROM ALL_ACCOUNTS WHERE account_number = %s", (acc_num,))
            account = self.cursor.fetchone()

            if not account:
                return "Account not found."
            
            # Check if the account type is "Fixed Deposit"
            if account[3] == "Fixed Deposit":  # Assuming account[3] is the account type column
                return "Withdrawals are not allowed from Fixed Deposit accounts."
            
            # Convert the current balance from Decimal to float
            current_balance = float(account[2])  # Assuming account[2] is the balance column
            
            # Check if there are sufficient funds for the withdrawal
            if current_balance >= amount:
                # Calculate the new balance after withdrawal
                new_balance = current_balance - amount
                
                # Execute the update query to modify the balance
                self.cursor.execute("UPDATE ALL_ACCOUNTS SET balance = %s WHERE account_number = %s", (new_balance, acc_num))
                self.db.commit()
                
                # Check if the update was successful
                if self.cursor.rowcount > 0:
                    return f"Withdrew {amount} from account {acc_num}. New balance: {new_balance}"
                else:
                    return "Withdrawal failed, no changes made."
            else:
                return "Insufficient balance."

        except ValueError:
            return "Invalid withdrawal amount."
        except mysql.connector.Error as err:
            return f"Error: {err}"

    def transfer(self, from_acc, to_acc, amount):
        try:
            # Convert the amount to float
            amount = float(amount)

            # Retrieve the "from" account details from the database
            self.cursor.execute("SELECT * FROM ALL_ACCOUNTS WHERE account_number = %s", (from_acc,))
            from_account = self.cursor.fetchone()

            # Retrieve the "to" account details from the database
            self.cursor.execute("SELECT * FROM ALL_ACCOUNTS WHERE account_number = %s", (to_acc,))
            to_account = self.cursor.fetchone()

            # Check if both accounts exist
            if not from_account or not to_account:
                return "One or both accounts not found."
            
            # Retrieve the balances of both accounts
            from_balance = float(from_account[2])  # Assuming account[2] is the balance column
            to_balance = float(to_account[2])  # Assuming account[2] is the balance column

            # Check if the "from" account has enough balance
            if from_balance >= amount:
                # Calculate new balances
                new_from_balance = from_balance - amount
                new_to_balance = to_balance + amount

                # Update the balance of the "from" account
                self.cursor.execute("UPDATE ALL_ACCOUNTS SET balance = %s WHERE account_number = %s", (new_from_balance, from_acc))

                # Update the balance of the "to" account
                self.cursor.execute("UPDATE ALL_ACCOUNTS SET balance = %s WHERE account_number = %s", (new_to_balance, to_acc))

                # Commit the changes to the database
                self.db.commit()

                # Check if the update was successful
                if self.cursor.rowcount > 0:
                    return f"Transferred {amount} from account {from_acc} to account {to_acc}. New balances: From: {new_from_balance}, To: {new_to_balance}"
                else:
                    return "Transfer failed, no changes made."

            else:
                return "Insufficient balance in the source account."

        except ValueError:
            return "Invalid transfer amount."
        except mysql.connector.Error as err:
            return f"Error: {err}"

    def display_account(self, acc_num):
            try:
                query = "SELECT * FROM ALL_ACCOUNTS WHERE account_number = %s"
                self.cursor.execute(query, (acc_num,))
                account = self.cursor.fetchone()
                if account:
                    account_details = {
                        "Account Number": account[0],
                        "Account Holder Name": account[1],
                        "Balance": account[2],
                        "Account Type": account[3],
                        "Bank Name": account[4],
                    }
                    return account_details
                else:
                    return "Account not found."
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return "An error occurred while retrieving account information."
    def delete_account(self, acc_num):
        try:
            # Check if the account exists in the database
            self.cursor.execute("SELECT * FROM ALL_ACCOUNTS WHERE account_number = %s", (acc_num,))
            account = self.cursor.fetchone()
            
            if not account:
                # If account doesn't exist, show a message
                return "Account not found."
            
            # Perform the DELETE operation to remove the account
            self.cursor.execute("DELETE FROM ALL_ACCOUNTS WHERE account_number = %s", (acc_num,))
            self.db.commit()
            
            # Check if any row was affected (account was deleted)
            if self.cursor.rowcount > 0:
                return "Account deleted successfully."
            else:
                return "No account was deleted."
        
        except mysql.connector.Error as err:
            # If there's a MySQL error, show it
            return f"Error: {err}"



    def list_accounts(self):
        try:
            # Fetch data from the database
            self.cursor.execute("SELECT * FROM ALL_ACCOUNTS")
            accounts = self.cursor.fetchall()
            return accounts  # Return the fetched accounts as a list of tuples
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []


class BankApp:
    def __init__(self, root):
        self.bank = Bank()
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("2560x1440")
        self.root.configure(bg="#001f3f")  # Dark blue background

        self.create_login_screen()

    def create_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#013a63", padx=20, pady=20, relief="raised", bd=5)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text="Bank Management System", bg="#013a63", fg="#ffffff",
                 font=("Helvetica", 28, "bold")).pack(pady=20)

        tk.Label(frame, text="Username", bg="#013a63", fg="#d9faff", font=("Helvetica", 16)).pack(anchor="w", pady=(10, 0))
        username_entry = tk.Entry(frame, font=("Helvetica", 14), width=30)
        username_entry.pack(pady=(0, 20))

        tk.Label(frame, text="Password", bg="#013a63", fg="#d9faff", font=("Helvetica", 16)).pack(anchor="w", pady=(10, 0))
        password_entry = tk.Entry(frame, font=("Helvetica", 14), show="*", width=30)
        password_entry.pack(pady=(0, 20))

        def login_action():
            username = username_entry.get()
            password = password_entry.get()
            if self.bank.login(username, password):
                self.show_message("Login Successful", "Welcome to the Bank Management System")
                self.show_welcome_popup()  # New method to show the welcome popup
                self.create_dashboard()
            else:
                self.show_message("Login Failed", "Invalid username or password.", error=True)

        tk.Button(frame, text="Login", command=login_action, font=("Helvetica", 16), bg="#0074D9", fg="#ffffff",
                  relief="solid", width=15, height=1).pack()

    def show_message(self, title, message, error=False):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.configure(bg="#001f3f")
        
        # Center the popup window
        self.center_window(popup, 400, 400)

        tk.Label(popup, text=title, font=("Helvetica", 18, "bold"), bg="#001f3f", fg="#ffffff").pack(pady=10)
        tk.Label(popup, text=message, font=("Helvetica", 14), bg="#001f3f",
                 fg="#ff4136" if error else "#2ecc40", wraplength=350, justify="center").pack(pady=10)

        tk.Button(popup, text="OK", command=popup.destroy, bg="#0074D9", fg="#ffffff",
                  font=("Helvetica", 14), width=10).pack(pady=10)

        popup.transient(self.root)
        popup.grab_set()

    def show_welcome_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Welcome")
        popup.configure(bg="#001f3f")
        
        # Center the popup window
        self.center_window(popup, 400, 400)

        tk.Label(popup, text="Welcome to the Bank Management System", font=("Helvetica", 18, "bold"), bg="#001f3f", fg="#ffffff").pack(pady=10)
        tk.Label(popup, text="You are now logged in.", font=("Helvetica", 14), bg="#001f3f", fg="#ffffff").pack(pady=10)

        tk.Button(popup, text="OK", command=popup.destroy, bg="#0074D9", fg="#ffffff", font=("Helvetica", 14), width=10).pack(pady=10)

        popup.transient(self.root)
        popup.grab_set()

    def create_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Bank Management Dashboard", bg="#001f3f", fg="#ffffff",
                 font=("Helvetica", 24, "bold")).pack(pady=20)

        buttons_frame = tk.Frame(self.root, bg="#001f3f")
        buttons_frame.pack(pady=10)

        # Create grid layout for the options
        options = [
            ("Create Account", self.create_account_screen),
            ("Update Account", self.update_account_screen),
            ("View Account", self.view_account_screen),
            ("Delete Account", self.delete_account_screen),
            ("Deposit", self.deposit_screen),
            ("Withdraw", self.withdraw_screen),
            ("Transfer", self.transfer_screen),
            ("List All Accounts", self.list_all_accounts_screen),
            ("Logout", self.logout_screen)
        ]

        for i, (text, command) in enumerate(options):
            row = i // 3
            col = i % 3
            tk.Button(buttons_frame, text=text, command=command, font=("Helvetica", 14),
                      bg="#0074D9", fg="#ffffff", width=20, height=2).grid(row=row, column=col, padx=10, pady=10)

    def create_account_screen(self):
        fields = ["Bank Name", "Account Number", "Account Holder Name", "Account Type", "Balance"]
        self.popup_form("Create Account", self.bank.create_account, fields)

    def update_account_screen(self):
        def update_account_action(acc_num, new_name, new_balance, new_acc_type):
            # Perform database operations to update the account
            try:
                # Check if the account exists in the database
                self.bank.cursor.execute("SELECT * FROM ALL_ACCOUNTS WHERE account_number = %s", (acc_num,))
                account = self.bank.cursor.fetchone()
                if not account:
                    return "No account found with the given account number."  # Return message instead of showing it directly

                # Update name, balance, and account type if provided
                update_values = []
                query = "UPDATE ALL_ACCOUNTS SET "
                if new_name:
                    query += "account_holder_name = %s, "
                    update_values.append(new_name)
                if new_balance:
                    query += "balance = %s, "
                    update_values.append(float(new_balance))
                if new_acc_type:
                    query += "account_type = %s, "
                    update_values.append(new_acc_type)
                
                # Remove the trailing comma and space
                query = query.rstrip(", ")

                # Add the WHERE condition to specify the account number
                query += " WHERE account_number = %s"
                update_values.append(acc_num)

                # Execute the update query
                self.bank.cursor.execute(query, tuple(update_values))
                self.bank.db.commit()

                # Check if any row was affected (updated)
                if self.bank.cursor.rowcount > 0:
                    return "Account details updated successfully."  # Return success message
                else:
                    return "No changes were made to the account."  # Return failure message
            except mysql.connector.Error as err:
                return f"Error: {err}"  # Return error message instead of showing it directly

        # Show the popup form for updating account and handle the result display
        self.popup_form("Update Account", update_account_action, 
                        ["Account Number", "New Account Holder Name", "New Account Balance", "New Account Type"])


    def view_account_screen(self):
        def display_account_action(acc_num):
            account_details = self.bank.display_account(acc_num)
            if isinstance(account_details, dict):
                message = "\n".join(f"{key}: {value}" for key, value in account_details.items())
            else:
                message = account_details
            return message  # Instead of showing the message directly here

        # In the popup_form method, show the message once after getting the result
        self.popup_form("View Account", display_account_action, ["Account Number"])


    def delete_account_screen(self):
        def delete_account_action(acc_num):
            # Perform account deletion and return the result
            return self.bank.delete_account(acc_num)  # Return the result instead of showing it directly

        # Show the popup form for deleting an account
        self.popup_form("Delete Account", delete_account_action, ["Account Number"])

    def deposit_screen(self):
        def deposit_action(acc_num, amount):
            # Perform deposit and return the result
            try:
                # Validate the amount
                amount = float(amount)
                if amount <= 0:
                    return "Deposit amount must be greater than zero."

                return self.bank.deposit(acc_num, amount)  # Return the result instead of showing it directly
            except ValueError:
                return "Invalid amount. Please enter a numeric value."

        # Show the popup form for deposit
        self.popup_form("Deposit", deposit_action, ["Account Number", "Amount"])


    def withdraw_screen(self):
        fields = ["Account Number", "Amount"]
        self.popup_form("Withdraw", self.bank.withdraw, fields)

    def transfer_screen(self):
        fields = ["From Account", "To Account", "Amount"]
        self.popup_form("Transfer", self.bank.transfer, fields)

    def list_all_accounts_screen(self):
        accounts = self.bank.list_accounts()
        if not accounts:
            self.show_message("No Accounts", "No accounts found.", error=True)
            return

        popup = tk.Toplevel(self.root)
        popup.title("List All Accounts")
        popup.configure(bg="#001f3f")

        self.center_window(popup, 800, 500)

        tree = ttk.Treeview(popup, columns=("Account Number", "Account Holder Name", "Balance", "Account Type", "Bank Name"), show="headings")
        tree.pack(fill="both", expand=True)

        tree.heading("Account Number", text="Account Number")
        tree.heading("Account Holder Name", text="Account Holder Name")
        tree.heading("Balance", text="Balance")
        tree.heading("Account Type", text="Account Type")
        tree.heading("Bank Name", text="Bank Name")

        for account in accounts:
            tree.insert("", "end", values=account)

    def logout_screen(self):
        self.bank.logged_in_user = None
        self.show_message("Logout Successful", "You have been logged out.", error=False)
        self.create_login_screen()

    def popup_form(self, title, action, fields):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.configure(bg="#001f3f")
        
        self.center_window(popup, 400, 550)

        frame = tk.Frame(popup, bg="#013a63", padx=20, pady=20, relief="raised", bd=5)
        frame.pack(padx=20, pady=20)

        entries = {}
        for field in fields:
            tk.Label(frame, text=field, bg="#013a63", fg="#ffffff", font=("Helvetica", 14)).pack(anchor="w", pady=(10, 0))
            entry = tk.Entry(frame, font=("Helvetica", 14), width=30)
            entry.pack(pady=(0, 10))
            entries[field] = entry

        def submit_action():
            # Collect field values and pass to action function
            args = [entries[field].get() for field in fields]
            result = action(*args)  # Get the result from action
            self.show_message(title, result)  # Show the result only once
            popup.destroy()  # Close the popup after showing the message

        tk.Button(frame, text="Submit", command=submit_action, font=("Helvetica", 14), bg="#0074D9", fg="#ffffff", width=20, height=2).pack(pady=10)


    def center_window(self, window, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        window.geometry(f'{width}x{height}+{position_right}+{position_top}')


if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
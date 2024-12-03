Bank Management System (BMS)

This software was made by Team Code Crusaders

Members:

1.AMAN YATI

2.ANSH SABHNANI

3.DHRUV GAGNANI

4.ANKIT KUMAR

Overview

The Bank Management System (BMS) is a software solution designed to streamline and automate banking processes, allowing banks to manage customer accounts, transactions, and related services efficiently. This system provides users with features such as account creation, deposits, withdrawals, account updates, and more, all while ensuring secure data handling and user-friendly interfaces.
Features

    Account Management:
        Create new accounts.
        View account details.
        Update account information (name, balance, account type).
        Delete accounts.

    Transaction Management:
        Deposit funds into accounts.
        Withdraw funds from accounts.
        Transfer money between accounts.

    Secure Authentication:
        User login and authentication.
        Password encryption for security.

    Real-time Data Updates:
        Ensure data consistency with live updates during transactions and account changes.

    User-Friendly Interface:
        Easy-to-use graphical user interface (GUI) for managing banking operations.

Technologies Used

    Frontend:
        Python (Tkinter for GUI)

    Backend:
        Python (for business logic and database operations)
        MySQL (for storing and retrieving account data)

    Security:
        Password encryption using hashing algorithms.
        Secure database connections.

Getting Started
Prerequisites

Before you begin, ensure you have the following installed:

    Python 3.x: Download Python
    MySQL: Download MySQL
    MySQL Connector for Python: Install using pip install mysql-connector-python
    Tkinter: Usually comes pre-installed with Python (if not, you can install it via pip install tk)


Set up the MySQL database:

    Create a database (e.g., bank_db) in MySQL.
    Run the provided SQL scripts (found in database/ folder) to create necessary tables like ALL_ACCOUNTS.

Run the project:

    python bms.py

Usage

    On running the application, you will be presented with a graphical user interface (GUI).
    You can create a new bank account, view account details, update information, and perform transactions (deposit/withdraw).
    The system will handle backend database operations automatically.

Limitations

    The application currently supports basic account management and transaction operations. Features like loan management, customer services, and advanced reporting are not included.
    The security is relatively simple (password hashing) and might not be sufficient for production-level banking systems.
    The application does not support multi-user functionality; it is designed for single-user interaction.

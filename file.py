import sqlite3
import os
import hashlib
import requests

# Hardcoded credentials (Security Issue)
USERNAME = "admin"
PASSWORD = "password123"

# Connect to SQLite database (insecure because no input sanitization)
conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")

# Insecure user login with SQL Injection vulnerability
def login(username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    if user:
        print(f"Welcome {username}!")
    else:
        print("Invalid credentials!")

# OS Command Injection vulnerability
def run_command():
    cmd = input("Enter command: ")  # Unsafe input
    os.system(cmd)  # Executes user input as a shell command

# Insecure MD5 Hashing (Weak Encryption)
def insecure_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

# Insecure External API Call (No SSL Verification)
def get_data():
    url = "http://example.com/api"  # Not using HTTPS
    response = requests.get(url, verify=False)  # Disabling SSL verification (BAD!)
    print(response.text)

# Main function
if __name__ == "__main__":
    print("Vulnerable Python App")
    while True:
        print("1. Login")
        print("2. Run Command")
        print("3. Get Data")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login(username, password)
        elif choice == "2":
            run_command()
        elif choice == "3":
            get_data()
        elif choice == "4":
            break
        else:
            print("Invalid choice, try again.")

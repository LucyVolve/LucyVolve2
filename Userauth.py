import tkinter as tk
from tkinter import messagebox
import psycopg2
import bcrypt
from postgres_db import connect

# Database connection function
# def connect_db():
#     return psycopg2.connect(
#         dbname="your_db_name",
#         user="your_username",
#         password="your_password",
#         host="localhost",
#         port="5432"
#     )

# Function to register a new user
def register_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with connect() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO Users (username, password_hash) VALUES (%s, %s)", (username, hashed))
                conn.commit()
                messagebox.showinfo("Success", "User registered successfully!")
            except Exception as e:
                messagebox.showerror("Registration Error", str(e))

# Function to log in a user
def login_user(username, password):
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT password_hash FROM Users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                messagebox.showinfo("Login Success", "Welcome!")
            else:
                messagebox.showerror("Login Error", "Invalid username or password.")

# Tkinter application class
class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Authentication")

        # Registration section
        tk.Label(self.root, text="Register").grid(row=0, column=0, columnspan=2)
        tk.Label(self.root, text="Username").grid(row=1, column=0)
        self.reg_username = tk.Entry(self.root)
        self.reg_username.grid(row=1, column=1)
        tk.Label(self.root, text="Password").grid(row=2, column=0)
        self.reg_password = tk.Entry(self.root, show="*")
        self.reg_password.grid(row=2, column=1)
        tk.Button(self.root, text="Register", command=self.register).grid(row=3, columnspan=2)

        # Login section
        tk.Label(self.root, text="Login").grid(row=4, column=0, columnspan=2)
        tk.Label(self.root, text="Username").grid(row=5, column=0)
        self.login_username = tk.Entry(self.root)
        self.login_username.grid(row=5, column=1)
        tk.Label(self.root, text="Password").grid(row=6, column=0)
        self.login_password = tk.Entry(self.root, show="*")
        self.login_password.grid(row=6, column=1)
        tk.Button(self.root, text="Login", command=self.login).grid(row=7, columnspan=2)

    def register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        if username and password:
            register_user(username, password)
        else:
            messagebox.showerror("Input Error", "All fields are required.")

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        if username and password:
            login_user(username, password)
        else:
            messagebox.showerror("Input Error", "All fields are required.")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext
from tkinter import font


def show_message(title, message):
    messagebox.showinfo(title, message)

def create_login_frame(window, login_callback, password_manager_frame, register_user_callback):
    login_frame = ttk.Frame(window, padding="10")
    login_frame.pack(fill='both', expand=True)

    ttk.Label(login_frame, text="Username:").pack(pady=(0, 5))
    username_entry = ttk.Entry(login_frame)
    username_entry.pack(pady=(0, 10))

    ttk.Label(login_frame, text="Password (won't be saved):").pack(pady=(0, 5))
    password_entry = ttk.Entry(login_frame, show="*")
    password_entry.pack(pady=(0, 10))

    button_frame = ttk.Frame(login_frame)
    button_frame.pack(fill='x', expand=True)

    register_button = ttk.Button(button_frame, text="Register", command=lambda: register_user_callback(username_entry.get(), password_entry.get()))
    register_button.pack(side=tk.LEFT, padx=(0, 10))

    login_button = ttk.Button(button_frame, text="Login", command=lambda: handle_login())
    login_button.pack(side=tk.RIGHT)



    def handle_login():
        if login_callback(username_entry.get(), password_entry.get()):
            login_frame.pack_forget()
            password_manager_frame.pack(fill='both', expand=True)
        else:
            show_message("Login", "Login Failed")

    return login_frame

def create_password_manager_frame(window, save_password_callback, load_passwords_callback, key):
    password_manager_frame = ttk.Frame(window, padding="10")

    ttk.Label(password_manager_frame, text="Website:").pack(pady=(0, 5))
    website_entry = ttk.Entry(password_manager_frame)
    website_entry.pack(pady=(0, 10))

    ttk.Label(password_manager_frame, text="Username/Email:").pack(pady=(0, 5))
    username_entry = ttk.Entry(password_manager_frame)
    username_entry.pack(pady=(0, 10))

    ttk.Label(password_manager_frame, text="Password:").pack(pady=(0, 5))
    password_entry = ttk.Entry(password_manager_frame, show="*")
    password_entry.pack(pady=(0, 10))

    save_button = ttk.Button(password_manager_frame, text="Save Password", command=lambda: handle_save_password())
    save_button.pack(pady=(0, 10))

    passwords_display = scrolledtext.ScrolledText(password_manager_frame, height=10)
    passwords_display.pack(fill='both', expand=True)

    load_button = ttk.Button(password_manager_frame, text="Load Passwords", command=lambda: handle_load_passwords())
    load_button.pack()

    def handle_save_password():
        if save_password_callback(website_entry.get(), username_entry.get(), password_entry.get(), key):
            show_message("Success", "Password saved successfully")
        else:
            show_message("Error", "Error saving password")

    def handle_load_passwords():
        passwords_display.delete(1.0, tk.END)
        passwords = load_passwords_callback(key)
        for website, user, password in passwords:
            passwords_display.insert(tk.END, f"Website: {website}, Username: {user}, Password: {password}\n")

    return password_manager_frame

def create_main_window(key, login_callback, save_password_callback, load_passwords_callback, register_user_callback):
    window = tk.Tk()
    window.title("Password Manager")
    
    window.resizable(True, True)
    window.configure(bg="#f2cda0")
    small_icon = tk.PhotoImage(file="16x16.png")
    large_icon = tk.PhotoImage(file="32x32.png")
    window.iconphoto(False, large_icon, small_icon)



    password_manager_frame = create_password_manager_frame(window, save_password_callback, load_passwords_callback, key)
    login_frame = create_login_frame(window, login_callback, password_manager_frame, register_user_callback)

    return window

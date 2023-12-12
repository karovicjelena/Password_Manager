import bcrypt
import os
from cryptography.fernet import Fernet
import gui
from tkinter import messagebox



KEY_FILE = 'secret.key'
USERS_FILE = 'users.txt'
current_user = None

def create_or_load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        return key

def hash_password(password): 
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def get_stored_hashed_password(username):
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            for line in file:
                stored_username, stored_hash = line.strip().split(':')
                if username == stored_username:
                    return stored_hash.encode()
    return None

def user_exists(username):
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            for line in file:
                stored_username, _ = line.strip().split(':')
                if stored_username == username:
                    return True
    return False

def register_user(username, password):
    if user_exists(username):
        messagebox.showerror("Registration Failed", "User already exists.")
        return False

    hashed_password = hash_password(password)
    with open(USERS_FILE, 'a') as file:
        file.write(f"{username}:{hashed_password.decode()}\n")

    messagebox.showinfo("Registration Successful", "User has been registered successfully.")
    return True


def login_callback(username, password):
    global current_user
    hashed_password = get_stored_hashed_password(username)
    if hashed_password and bcrypt.checkpw(password.encode(), hashed_password):
        current_user = username
        return True
    else:
        messagebox.showerror("Login Failed", "Wrong username or password.")
        return False


def get_user_file(username):
    return f"data_{username}.txt"

def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

def decrypt_data(encrypted_data, key):
    fernet = Fernet(key) 
    return fernet.decrypt(encrypted_data).decode()

def save_user_password(website, username, password, key):
    if current_user:
        encrypted_password = encrypt_data(password, key)
        file_name = get_user_file(current_user)
        with open(file_name, 'a') as file:
            file.write(f"{website},{username},{encrypted_password.decode()}\n")
        return True
    return False

def load_user_passwords(key):
    if current_user:
        file_name = get_user_file(current_user)
        if not os.path.exists(file_name):
            return []

        passwords = []
        with open(file_name, 'r') as file:
            for line in file.readlines():
                website, username, encrypted_password = line.strip().split(',')
                decrypted_password = decrypt_data(encrypted_password.encode(), key)
                passwords.append((website, username, decrypted_password))
        return passwords
    return []

def main():
    key = create_or_load_key()
    main_window = gui.create_main_window(key, login_callback, save_user_password, load_user_passwords, register_user)
    main_window.mainloop()

if __name__ == "__main__":
    main()


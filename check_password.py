import customtkinter as ctk
from tkinter import messagebox
import os
from APP import App
from cryptography.fernet import Fernet

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)

key_path = os.path.join(parent_directory, "Password-Manager(CustomTkinter)/data", "key.txt")
password_path = os.path.join(parent_directory, "Password-Manager(CustomTkinter)/data", "password.txt")

if not os.path.exists(key_path):
    KEY = Fernet.generate_key()
    CIPHER_SUITE = Fernet(KEY)
    with open(key_path, "wb") as key_file:
        key_file.write(KEY)
else:
    with open(key_path, "rb") as key_file:
        KEY = key_file.read()
        CIPHER_SUITE = Fernet(KEY)


class Password(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.attempt = ""
        self.password = ""
        self.decrypted_password = ""
        self.confirmation = ""
        self.title(f"Yevhen's Password Manager")
        self.geometry("250x150+700+350")
        self.resizable(False, False)  # Width, Height

        self.enter_button = ctk.CTkButton(self, text="Enter",
                                          command=self.enter_dialog)
        self.enter_button.grid(row=1, column=2, padx=60, pady=10)
        self.password_label = ctk.CTkLabel(self, text=f"Please Enter your password")
        self.password_label.grid(row=0, column=2, padx=50, pady=20)
        # self.password_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(self.password_window))

    def enter_dialog(self):
        if os.path.exists(password_path):
            with open(password_path, "rb") as file:
                saved_password = file.read()
            self.decrypted_password = CIPHER_SUITE.decrypt(saved_password).decode()
            entry = ctk.CTkInputDialog(title="Enter Password", text="Enter your password:")
            entry.geometry("700+350")
            self.attempt = entry.get_input()
            self.check_password()
        else:
            password_input = ctk.CTkInputDialog(title="Create Password", text="Create a new password:")
            password_input.geometry("700+350")
            self.password = password_input.get_input()
            confirmation_input = ctk.CTkInputDialog(title="Confirm Password", text="Confirm your password:")
            confirmation_input.geometry("700+350")
            self.confirmation = confirmation_input.get_input()
            self.check_inputs()

    def check_inputs(self):
        if self.password == self.confirmation:
            with open(password_path, "wb") as file:
                encrypted_password = CIPHER_SUITE.encrypt(self.password.encode())
                file.write(encrypted_password)
            self.destroy()
            app = App()
            app.mainloop()
        else:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")

    def check_password(self):
        if self.decrypted_password == self.attempt:
            self.destroy()
            app = App()
            app.mainloop()
        else:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")

    # def on_closing(self, window):
    #     window.destroy()
    #     self.quit()


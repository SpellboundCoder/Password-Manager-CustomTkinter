import customtkinter as ctk
import pyclip


class NewWindow(ctk.CTk):
    def __init__(self, website, data):
        super().__init__()
        self.data = data
        self.website = website
        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title(f"{self.website}")
        self.new_window.geometry("350x120")
        self.new_window.resizable(False, True)  # Width, Height
        self.new_window.attributes("-topmost", True)
        self.lift()
        self.email_button = ctk.CTkButton(self.new_window, text="Copy Email", command=self.copy_email)
        self.email_button.grid(row=0, column=1, padx=10, pady=20)
        self.password_button = ctk.CTkButton(self.new_window, text="Copy Password", command=self.copy_password)
        self.password_button.grid(row=1, column=1, padx=10, pady=10)
        self.email_label = ctk.CTkLabel(self.new_window, text=f"{self.data[website]['email']}")
        self.password_label = ctk.CTkLabel(self.new_window, text=f"{self.data[website]['password']}")
        self.email_label.grid(row=0, column=0, padx=10, pady=20)
        self.password_label.grid(row=1, column=0, padx=10, pady=10)

    def copy_email(self):
        pyclip.copy(self.data[self.website]['email'])

    def copy_password(self):
        pyclip.copy(self.data[self.website]['password'])

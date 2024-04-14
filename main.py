import customtkinter as ctk
from check_password import Password

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

if __name__ == "__main__":
    password = Password()
    password.mainloop()

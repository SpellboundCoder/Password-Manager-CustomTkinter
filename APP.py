import customtkinter as ctk
from PIL import Image
import pyclip
import json
import string
import random
from new_window import NewWindow
from tkinter import messagebox


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Yevhen's Password Manager.py")
        self.geometry("700x470+500+250")
        self.data = {
            "Websitetest": {
                "email": "firstemailtest@gmail.com",
                "password": "test_password"
            }
        }
        # open data.json file
        try:
            with open("data/data.json", 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data/data.json", 'w') as data_file:
                json.dump(self.data, data_file, indent=4)
        else:
            self.data = data

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # password generator
        self.password_characters = string.ascii_letters + string.digits + string.punctuation
        self.password = " "
        # Adjust the length of the password here
        self.password_length = 12
        self.new_password_length = 12
        # load images with light and dark mode image
        self.add_icon = ctk.CTkImage(Image.open("Images/add_button.png"), size=(20, 20))
        self.saved_icon = ctk.CTkImage(Image.open("Images/saved.png"), size=(20, 20))
        self.delete_icon = ctk.CTkImage(Image.open("Images/delete_.png"), size=(20, 20))
        self.change_icon = ctk.CTkImage(Image.open("Images/change.png"), size=(20, 20))
        self.search_icon = ctk.CTkImage(Image.open("Images/search_11.png"), size=(20, 20))
        self.large_image = ctk.CTkImage(Image.open("Images/logo.png"), size=(300, 200))
        self.delete_frame_image = ctk.CTkImage(Image.open("Images/logo.png"), size=(300, 250))
        self.home_image = ctk.CTkImage(light_image=Image.open("Images/logo.png"),
                                       dark_image=Image.open("Images/logo.png"), size=(25, 25))
        self.lock_image = ctk.CTkImage(light_image=Image.open("Images/logo.png"),
                                       dark_image=Image.open("Images/logo.png"), size=(20, 20))
        self.choose_email = ctk.CTkImage(light_image=Image.open("Images/mail-red.png"),
                                         dark_image=Image.open("Images/mail-red.png"), size=(18, 18))
        self.reset_password = ctk.CTkImage(light_image=Image.open("Images/password-reset.png"),
                                           dark_image=Image.open("Images/password-reset.png"), size=(20, 20))
        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="Password Manager",
                                                   image=self.home_image,
                                                   compound="right",
                                                   font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        # Frame 1 (home)
        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                         text="Create Password",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"),
                                         image=self.add_icon, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")
        # Frame 2 (saved passwords)
        self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                            border_spacing=10, text="Saved Passwords",
                                            fg_color="transparent", text_color=("gray10", "gray90"),
                                            hover_color=("gray70", "gray30"),
                                            image=self.saved_icon, anchor="w",
                                            command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        # Frame 3 (change password)
        self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                            border_spacing=10, text="Change Password",
                                            fg_color="transparent", text_color=("gray10", "gray90"),
                                            hover_color=("gray70", "gray30"),
                                            image=self.change_icon, anchor="w",
                                            command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        # Frame 4 (delete password)
        self.frame_4_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                            border_spacing=10, text="Delete Password",
                                            fg_color="transparent", text_color=("gray10", "gray90"),
                                            hover_color=("gray70", "gray30"),
                                            image=self.delete_icon, anchor="w",
                                            command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame,
                                                      values=["Dark", "Light", "System"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # CREATE HOME FRAME
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text="",
                                                         image=self.large_image)
        self.home_frame_large_image_label.grid(row=0, column=0, columnspan=4, pady=10)

        # WEBSITE and Search
        self.home_label_password = ctk.CTkLabel(self.home_frame, text="Website:",
                                                font=ctk.CTkFont(size=15, weight="bold"))
        self.home_label_password.grid(row=1, column=0, pady=10)
        self.home_entry_website = ctk.CTkEntry(self.home_frame, placeholder_text="Enter a Website Here",
                                               text_color="orange")
        self.home_entry_website.grid(row=1, column=1, pady=(10, 10), sticky="nsew")
        self.home_button_search = ctk.CTkButton(self.home_frame, text="Search Website",
                                                image=self.search_icon, compound="right",
                                                command=self.search_password)
        self.home_button_search.grid(row=1, column=3, pady=10)

        # USERNAME/EMAIL
        self.home_label_email = ctk.CTkLabel(self.home_frame, text="Email/Username:",
                                             font=ctk.CTkFont(size=15, weight="bold"))
        self.home_label_email.grid(row=2, column=0, pady=(10, 10))
        self.home_entry_email = ctk.CTkEntry(self.home_frame,
                                             text_color="orange",
                                             placeholder_text="Enter Email/Username Here")
        self.home_entry_email.grid(row=2, column=1, pady=(10, 10), sticky="nsew")
        self.home_option_mails = ctk.CTkOptionMenu(self.home_frame, dynamic_resizing=False,
                                                   values=["yevgenphk@gmail.com",
                                                           "krivtsov357@gmail.com",
                                                           "mljonnypro@gmail.com",
                                                           "inna.aleksandrova.93@gmail.com"],
                                                   command=self.choice_of_email)
        self.home_option_mails.grid(row=2, column=3, pady=10)
        self.home_option_mails.set("Choose Email")

        # length of password
        self.home_label_password_length = ctk.CTkLabel(self.home_frame, text="Length(8-16):",
                                                       font=ctk.CTkFont(size=15,
                                                                        weight="bold"))
        self.home_label_password_length.grid(row=3, column=0, pady=10)
        self.home_entry_password_length = ctk.CTkEntry(self.home_frame, text_color="orange")
        self.home_entry_password_length.grid(row=3, column=1, columnspan=1, pady=(10, 10), sticky="nsew")
        self.home_entry_password_length.insert(0, self.password_length)
        self.slider = ctk.CTkSlider(self.home_frame, width=100, from_=8, to=16, number_of_steps=4,

                                    command=self.update_length)
        self.slider.grid(row=3, column=3, pady=(10, 10), sticky="ew")

        # generate password
        self.home_label_password = ctk.CTkLabel(self.home_frame, text="Password:",
                                                font=ctk.CTkFont(size=15, weight="bold"))
        self.home_label_password.grid(row=4, column=0, pady=10)
        self.home_entry_password = ctk.CTkEntry(self.home_frame, text_color="orange")
        self.home_entry_password.grid(row=4, column=1, pady=(10, 10), sticky="nsew")
        self.home_frame_button_generate_password = ctk.CTkButton(self.home_frame, text="Generate Password",
                                                                 command=self.generate_password)
        self.home_frame_button_generate_password.grid(row=4, column=3, padx=10, pady=10)

        # create "ADD" button
        self.home_frame_button_add = ctk.CTkButton(self.home_frame, width=290, text="Add Password",
                                                   image=self.add_icon, compound="right", command=self.save)
        self.home_frame_button_add.grid(row=5, column=1, columnspan=3, padx=(0, 10), pady=(10, 10))

        # CREATE CHANGE_PASSWORD FRAME
        self.change_password_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.change_password_frame.grid_columnconfigure(0, weight=1)

        self.change_frame_large_image_label = ctk.CTkLabel(self.change_password_frame, text="",
                                                           image=self.large_image)
        self.change_frame_large_image_label.grid(row=0, column=0, columnspan=4, pady=10)
        # Change password items
        self.change_password_label = ctk.CTkLabel(self.change_password_frame, text="Website:",
                                                  font=ctk.CTkFont(size=15, weight="bold"))
        self.change_password_label.grid(row=1, column=0, pady=10)
        self.chg_psw_entry_website = ctk.CTkEntry(self.change_password_frame, placeholder_text="Enter a Website Here",
                                                  text_color="orange")
        self.chg_psw_entry_website.grid(row=1, column=1, pady=(10, 10), sticky="nsew")
        self.change_button_search = ctk.CTkButton(self.change_password_frame, text="Search Website",
                                                  image=self.search_icon, compound="right",
                                                  command=self.search_password_frame3)
        self.change_button_search.grid(row=1, column=3, pady=10)

        # Shows Email and Password for chosen Website

        self.change_label_email = ctk.CTkLabel(self.change_password_frame, text="Email/Password:",
                                               font=ctk.CTkFont(size=15, weight="bold"))
        self.change_label_email.grid(row=2, column=0, pady=(10, 10))
        self.chosen_website_email_entry = ctk.CTkEntry(self.change_password_frame,
                                                       text_color="orange",
                                                       placeholder_text="Email")
        self.chosen_website_email_entry.grid(row=2, column=1, pady=(10, 10), sticky="nsew")
        self.chosen_website_password_entry = ctk.CTkEntry(self.change_password_frame,
                                                          text_color="orange",
                                                          placeholder_text="Password")
        self.chosen_website_password_entry.grid(row=2, column=3, pady=(10, 10), padx=5, sticky="nsew")

        # length of password ( change_password - frame )
        self.change_label_password_length = ctk.CTkLabel(self.change_password_frame, text="Length(8-16):",
                                                         font=ctk.CTkFont(size=15, weight="bold"))
        self.change_label_password_length.grid(row=3, column=0, pady=10)
        self.change_entry_password_length = ctk.CTkEntry(self.change_password_frame, text_color="orange")
        self.change_entry_password_length.grid(row=3, column=1, columnspan=1, pady=(10, 10), sticky="nsew")
        self.change_entry_password_length.insert(0, self.password_length)
        self.slider_change_password = ctk.CTkSlider(self.change_password_frame, width=100, from_=8, to=16,
                                                    number_of_steps=4,
                                                    command=self.update_length_frame3)
        self.slider_change_password.grid(row=3, column=3, pady=(10, 10), sticky="ew")

        # generate new password ( change_password frame )
        self.change_label_password = ctk.CTkLabel(self.change_password_frame, text="New Password:",
                                                  font=ctk.CTkFont(size=15, weight="bold"))
        self.change_label_password.grid(row=4, column=0, pady=10)
        self.change_entry_password = ctk.CTkEntry(self.change_password_frame, text_color="orange")
        self.change_entry_password.grid(row=4, column=1, pady=(10, 10), sticky="nsew")
        self.change_frame_button_generate_password = ctk.CTkButton(self.change_password_frame, text="Generate Password",
                                                                   command=self.generate_password_frame3)
        self.change_frame_button_generate_password.grid(row=4, column=3, padx=10, pady=10)

        #  "CHANGE_PASSWORD" button
        self.change_frame_button_add = ctk.CTkButton(self.change_password_frame, width=290, text="Change Password",
                                                     image=self.change_icon, compound="right",
                                                     command=self.update_password)
        self.change_frame_button_add.grid(row=5, column=1, columnspan=3, padx=(0, 10), pady=(10, 10))

        # CREATE A FRAME "Saved Passwords"
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.textbox = ctk.CTkTextbox(self.second_frame, width=460, height=450, scrollbar_button_color='green',
                                      scrollbar_button_hover_color='green', text_color=("black", "orange"))
        self.textbox.grid(row=0, column=0, columnspan=3, padx=(20, 20), pady=(10, 10), sticky="nsew")

        # Delete Frame
        self.delete_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.delete_frame.grid_columnconfigure(0, weight=1)

        self.delete_frame_large_image_label = ctk.CTkLabel(self.delete_frame, text="",
                                                           image=self.delete_frame_image)
        self.delete_frame_large_image_label.grid(row=0, column=0, columnspan=4, pady=25)

        # WEBSITE and Search
        self.delete_label_website = ctk.CTkLabel(self.delete_frame, text="Website:",
                                                 font=ctk.CTkFont(size=15, weight="bold"))
        self.delete_label_website.grid(row=1, column=0, pady=10)
        self.delete_entry_website = ctk.CTkEntry(self.delete_frame, placeholder_text="Enter a Website Here",
                                                 text_color="orange")
        self.delete_entry_website.grid(row=1, column=1, pady=(10, 10), sticky="nsew")
        self.delete_button_search = ctk.CTkButton(self.delete_frame, text="Search Website",
                                                  image=self.search_icon, compound="right",
                                                  command=self.search_password_frame4)
        self.delete_button_search.grid(row=1, column=3, pady=10)

        # SHOW Email/Password for Chosen Website
        self.delete_label_email = ctk.CTkLabel(self.delete_frame, text="Email/Password:",
                                               font=ctk.CTkFont(size=15, weight="bold"))
        self.delete_label_email.grid(row=2, column=0, pady=(10, 10))
        self.delete_email_entry = ctk.CTkEntry(self.delete_frame,
                                               text_color="orange",
                                               placeholder_text="Email")
        self.delete_email_entry.grid(row=2, column=1, pady=(10, 10), sticky="nsew")
        self.delete_password_entry = ctk.CTkEntry(self.delete_frame,
                                                  text_color="orange",
                                                  placeholder_text="Password")
        self.delete_password_entry.grid(row=2, column=3, pady=(10, 10), padx=5, sticky="nsew")

        # DELETE button
        self.delete_button = ctk.CTkButton(self.delete_frame, width=290, text="Delete Password",
                                           image=self.delete_icon, compound="right", command=self.delete)
        self.delete_button.grid(row=5, column=1, columnspan=3, padx=(0, 10), pady=(10, 10))

        # SELECT DEFAULT  FRAME
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.change_password_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.change_password_frame.grid_forget()
        if name == "frame_4":
            self.delete_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.delete_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")
        self.textbox.delete("0.0", "end")
        with open("data/data.json") as file:
            data = json.load(file)
        for key, value in data.items():
            self.textbox.insert("0.0",
                                f"Website:                     Email:                           Password:   \n"
                                f" {key}   |    {value['email']}   |    {value['password']}\n\n")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def generate_password(self):
        self.home_entry_password.delete(0, ctk.END)
        self.password = ''.join(random.choice(self.password_characters) for _ in range(self.password_length))
        pyclip.copy(self.password)
        self.home_entry_password.insert(0, self.password)

    def generate_password_frame3(self):
        self.change_entry_password.delete(0, ctk.END)
        self.password = ''.join(random.choice(self.password_characters) for _ in range(self.new_password_length))
        pyclip.copy(self.password)
        self.change_entry_password.insert(0, self.password)

    def update_length(self, value):
        self.home_entry_password_length.delete(0, ctk.END)
        self.home_entry_password_length.insert(0, int(value))
        self.password_length = int(value)

    def update_length_frame3(self, value):
        self.change_entry_password_length.delete(0, ctk.END)
        self.change_entry_password_length.insert(0, int(value))
        self.new_password_length = int(value)

    def search_password(self):
        website = self.home_entry_website.get()
        if website in self.data:
            NewWindow(website, self.data)
        else:
            messagebox.showinfo(title=website, message=f" '{website}' not in the list of your saved websites.")

    def search_password_frame3(self):
        website = self.chg_psw_entry_website.get()
        if website in self.data:
            self.chosen_website_email_entry.delete(0, ctk.END)
            self.chosen_website_email_entry.insert(0, self.data[website]['email'])
            self.chosen_website_password_entry.delete(0, ctk.END)
            self.chosen_website_password_entry.insert(0, self.data[website]['password'])
        else:
            messagebox.showinfo(title=website, message=f" '{website}' not in the list of your saved websites.")

    def search_password_frame4(self):
        website = self.delete_entry_website.get()
        if website in self.data:
            self.delete_email_entry.delete(0, ctk.END)
            self.delete_email_entry.insert(0, self.data[website]['email'])
            self.delete_password_entry.delete(0, ctk.END)
            self.delete_password_entry.insert(0, self.data[website]['password'])
        else:
            messagebox.showinfo(title=website, message=f" '{website}' not in the list of your saved websites.")

    def choice_of_email(self, value):
        self.home_entry_email.delete(0, ctk.END)
        self.home_entry_email.insert(0, value)

    def save(self):
        website = self.home_entry_website.get()
        email = self.home_entry_email.get()
        password = self.home_entry_password.get()
        new_data = {
            website: {
                "email": email,
                "password": password
            }
        }
        if len(website) == 0 or len(email) == 0 or len(password) == 0:
            messagebox.showwarning(title="Oops", message="Please don't leave any lines empty!")
        else:
            self.data.update(new_data)
            with open("data/data.json", "w") as data_file:
                json.dump(self.data, data_file, indent=4)
            self.home_entry_website.delete(0, ctk.END)
            self.home_entry_password.delete(0, ctk.END)
            self.home_entry_email.delete(0, ctk.END)
            messagebox.showinfo(title="New Record Created.", message=f"Website: '{website}'\n"
                                                                     f"Email: '{email}'\n"
                                                                     f"Password: '{password}'")

    def update_password(self):
        website = self.chg_psw_entry_website.get()
        email = self.chosen_website_email_entry.get()
        new_password = self.change_entry_password.get()
        self.data[website]["password"] = new_password

        if len(website) == 0 or len(email) == 0 or len(new_password) == 0:
            messagebox.showwarning(title="Oops", message="Please don't leave any lines empty!")
        else:
            # self.data.update(new_data)
            with open("data/data.json", "w") as data_file:
                json.dump(self.data, data_file, indent=4)
            self.chg_psw_entry_website.delete(0, ctk.END)
            self.chosen_website_password_entry.delete(0, ctk.END)
            self.chosen_website_email_entry.delete(0, ctk.END)
            self.change_entry_password.delete(0, ctk.END)
            messagebox.showinfo(title="Password updated", message=f"Website: '{website}'\n "
                                                                  f"New_Password: '{new_password}'")

            self.chg_psw_entry_website.configure(placeholder_text='Enter a Website')
            self.chosen_website_password_entry.configure(placeholder_text='Password')
            self.chosen_website_email_entry.configure(placeholder_text='Email')

    def delete(self):
        website_to_delete = self.delete_entry_website.get()
        if website_to_delete in self.data:
            del self.data[website_to_delete]
            with open("data/data.json", "w") as data_file:
                json.dump(self.data, data_file, indent=4)
            self.delete_entry_website.delete(0, ctk.END)
            self.delete_email_entry.delete(0, ctk.END)
            self.delete_password_entry.delete(0, ctk.END)
            messagebox.showinfo(title="Website deleted", message=f"Website: '{website_to_delete}'\n")
            self.delete_entry_website.configure(placeholder_text='Enter a Website')
            self.delete_email_entry.configure(placeholder_text='Password')
            self.delete_password_entry.configure(placeholder_text='Email')

        else:
            messagebox.showwarning('Chosen Website is not found, please check the name again')

from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = 4
    nr_symbols = 4
    nr_numbers = 4

    password = ""
    for n in range(0, nr_letters):
        index = random.randint(0, len(letters) - 1)
        password += letters[index]

    for n in range(0, nr_symbols):
        index = random.randint(0, len(symbols) - 1)
        password += symbols[index]

    for n in range(0, nr_numbers):
        index = random.randint(0, len(numbers) - 1)
        password += numbers[index]

    hard_pass = [password[n] for n in range(0, len(password))]
    random.shuffle(hard_pass)
    hard = ""
    for n in hard_pass:
        hard += n

    password_entry.delete(0, END)
    password_entry.insert(0, hard)
    pyperclip.copy(hard)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()

    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            messagebox.showinfo(
                title="Website Details",
                message=f"Website Name: {website} \nEmail: {data[website]['email']} "
                        f"\nPassword: {data[website]['password']}"
            )
        else:
            messagebox.showinfo(title="Sorry :(", message="No Details for the website exist")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any empty fields here")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- TOGGLE PASSWORD VISIBILITY ------------------------------- #
def toggle_password_visibility():
    current_show_state = password_entry["show"]
    if current_show_state == "*":
        password_entry["show"] = ""
        show_password_button.config(image=hide_img, command=toggle_password_visibility)
    else:
        password_entry["show"] = "*"
        show_password_button.config(image=show_img, command=toggle_password_visibility)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="#F0F0F0")

# Create a frame for the logo
logo_frame = Frame(window, bg="#F0F0F0")
logo_frame.grid(row=0, column=1, pady=(30, 20))

# Load the logo image
pass_img = PhotoImage(file="logo.png")

# Create a label with the logo image
logo_label = Label(logo_frame, image=pass_img, bg="#F0F0F0")
logo_label.grid(row=0, column=0)

# Create a label for the app title
title_label = Label(window, text="Password Manager", font=("Arial", 24, "bold"), bg="#F0F0F0")
title_label.grid(row=1, column=1, pady=(10, 20))

# Create labels and entry fields
website_label = Label(window, text="Website:", font=("Arial", 12), bg="#F0F0F0")
website_label.grid(row=2, column=0, padx=(0, 10), pady=(0, 10), sticky="w")
website_entry = Entry(window, width=50, font=("Arial", 12))
website_entry.grid(row=2, column=1, columnspan=2, pady=(0, 10))

email_label = Label(window, text="Email/Username:", font=("Arial", 12), bg="#F0F0F0")
email_label.grid(row=3, column=0, padx=(0, 10), pady=(0, 10), sticky="w")
email_entry = Entry(window, width=50, font=("Arial", 12))
email_entry.grid(row=3, column=1, columnspan=2, pady=(0, 10))

password_label = Label(window, text="Password:", font=("Arial", 12), bg="#F0F0F0")
password_label.grid(row=4, column=0, padx=(0, 10), pady=(0, 10), sticky="w")
password_entry = Entry(window, width=50, font=("Arial", 12), show="*")
password_entry.grid(row=4, column=1, pady=(0, 10))

# Add a button to generate password
generate_button = Button(window, text="Generate Password", command=generate_password, font=("Arial", 12), bg="#1B6B93",
                         fg="#F5F5F5")
generate_button.grid(row=4, column=3, padx=(10, 0), pady=(0, 10))

# Add an icon to toggle password visibility
show_img = PhotoImage(file="show.png")
hide_img = PhotoImage(file="hide.png")
show_password_button = Button(window, width=25, height=25, image=show_img, bg="#F0F0F0",
                              command=toggle_password_visibility)
show_password_button.grid(row=4, column=4, padx=(0, 10), pady=(0, 10))

# Add buttons to save and search passwords
save_button = Button(window, text="Add", width=50, command=save, font=("Arial", 12), bg="#4FC0D0")
save_button.grid(row=5, column=1, columnspan=2, pady=(0, 10))

search_button = Button(window, text="Search", width=15, command=find_password, font=("Arial", 12), bg="#A2FF86")
search_button.grid(row=2, column=3, padx=(10, 0), pady=(0, 10))

window.mainloop()

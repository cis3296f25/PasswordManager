import customtkinter

customtkinter.set_appearance_mode("dark")  # forces dark mode
customtkinter.set_default_color_theme("dark-blue")

def button_callback():
    print("button clicked")

app = customtkinter.CTk()
app.title("Offline Password Manager")
app.geometry("400x300")


button = customtkinter.CTkButton(app, text="my button", fg_color="green", command=button_callback)
button.grid(row=0, column=0, padx=20, pady=20)

app.mainloop()

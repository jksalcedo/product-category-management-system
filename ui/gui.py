import customtkinter as ctk

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# window
window = ctk.CTk()
window.title("Product Category Management System")
window.geometry("900x600")

# sidebar
sidebar = ctk.CTkFrame(window, width=180)
sidebar.pack(side="left", fill="y", padx=10, pady=10)

ctk.CTkLabel(sidebar, text="MENU", font=("Arial", 18, "bold")).pack(pady=10)
ctk.CTkButton(sidebar, text="Home", width=150).pack(pady=5)
ctk.CTkButton(sidebar, text="Categories", width=150).pack(pady=5)
ctk.CTkButton(sidebar, text="Products", width=150).pack(pady=5)
ctk.CTkButton(sidebar, text="Exit", width=150, command=window.destroy).pack(side="bottom", pady=10)


# main frame
main_frame = ctk.CTkFrame(window, width=180)
main_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)


# run
window.mainloop()
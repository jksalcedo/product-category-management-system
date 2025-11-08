# import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

class App(ctk.CTk):
    def __init__(self, title, size):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # widgets
        self.main = Main(self, width=180)
        self.sidebar = SideBar(self, main = self.main, width=180)

        # run
        self.mainloop()

class SideBar(ctk.CTkFrame):
    def __init__(self, parent, main, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side = "left", fill = "y", padx=10, pady=10)

        self.create_widgets(parent, main)

    def create_widgets(self, parent, main):
        # create the widgets
        ctk.CTkLabel(self, text="MENU", font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkButton(self, text="Home", width=150, command=main.show_home_tab).pack(pady=5)
        ctk.CTkButton(self, text="Categories", width=150, command=main.show_category_tab).pack(pady=5)
        ctk.CTkButton(self, text="Products", width=150, command=main.show_product_tab).pack(pady=5)
        ctk.CTkButton(self, text="Exit", width=150, command=parent.destroy).pack(side="bottom", pady=10)


class Main(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side="right", expand=True, fill='both', padx=10, pady=10)

        self.home_tab = HomeTab(self)
        self.category_tab = CategoryTab(self)
        self.product_tab = ProductTab(self)

        self.show_home_tab()

    def show_home_tab(self):
        self.home_tab.tkraise()

    def show_category_tab(self):
        self.category_tab.tkraise()

    def show_product_tab(self):
        self.product_tab.tkraise()

class HomeTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        ctk.CTkLabel(self, text="🏠 Home", font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(
            self,
            text="Welcome to the Product Category Management System!\n\nUse the sidebar to navigate through different sections.",
            justify="center",
            font=("Arial", 16)
        ).pack(pady=10)


class CategoryTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Header/Label
        ctk.CTkLabel(self, text="Category Management", font=("Arial", 20, "bold")).pack(pady=10)

        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        tree = ttk.Treeview(tree_frame)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=(5, 10), ipady=10, ipadx=5)

        ctk.CTkButton(button_frame, text="Add Category", command=self.add_category_popup).pack(side="left", padx=(10,5))
        ctk.CTkButton(button_frame, text="Edit Category", command=self.edit_category_popup).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Delete Category", fg_color="red", command=self.delete_category).pack(side="left", padx=(5,0))

    # ---------- HELPER ----------
    def load_products(self):
        """Reload product data from the database."""
        pass

    def add_category_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Category")
        popup.geometry("300x300")

    def edit_category_popup(self):
        print("Edit Category clicked")

    def delete_category(self):
        print("Delete Category clicked")


class ProductTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Header/Label
        ctk.CTkLabel(self, text="Product Management", font=("Arial", 20, "bold")).pack(pady=(10,5))

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.product_table = ttk.Treeview(
            table_frame, columns=("name", "price", "category"), show="headings")
        self.product_table.heading("name", text="Product Name")
        self.product_table.heading("price", text="Price (₱)")
        self.product_table.heading("category", text="Category")
        self.product_table.pack(expand=True, fill="both", padx=10, pady=10)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=(5, 10), ipady=10, ipadx=5)

        ctk.CTkButton(button_frame, text="Add Product", command=self.add_product_popup).pack(side="left", padx=(10,5))
        ctk.CTkButton(button_frame, text="Edit Product", command=self.edit_product_popup).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Delete Product", fg_color="red", command=self.delete_product).pack(side="left", padx=(5,0))

        # Load Products from Database
        self.load_products()

    # ---------- HELPER ----------
    def load_products(self):
        """Reload product data from the database."""
        pass

    def add_product_popup(self):
        popup = ctk.CTkToplevel()
        popup.title("Add Product")
        popup.geometry("300x300")

    def edit_product_popup(self):
        print("Edit Product clicked")

    def delete_product(self):
        print("Delete Product clicked")


class Entry(ctk.CTkFrame):
    def __init__(self, parent, label_text, button_text, label_background):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text=label_text)
        button = ctk.CTkButton(self, text=button_text)

        label.pack(expand=True, fill='both')
        button.pack(expand=True, fill='both', pady=10)

        self.pack(side='left', expand=True, fill='both', padx=20, pady=20)


App('Class based app with ctk', (900, 600))
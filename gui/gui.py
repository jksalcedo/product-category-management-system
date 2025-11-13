# import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import database.db_manager as db  # Added database import

class App(ctk.CTk):
    def __init__(self, title, size):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # Initialize database
        try:
            db.initialize_database()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")

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
        ctk.CTkButton(self, text="Category Hierarchy", width=150, command=main.show_category_hierarchy).pack(pady=5)
        ctk.CTkButton(self, text="Exit", width=150, command=parent.destroy).pack(side="bottom", pady=10)


class Main(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side="right", expand=True, fill='both', padx=10, pady=10)

        self.home_tab = HomeTab(self)
        self.category_tab = CategoryTab(self)
        self.product_tab = ProductTab(self)
        self.category_hierarchy = CategoryHierarchyTab(self)

        self.show_home_tab()

    def show_home_tab(self):
        self.home_tab.tkraise()

    def show_category_tab(self):
        self.category_tab.load_categories()  # ensure refresh
        self.category_tab.tkraise()

    def show_product_tab(self):
        self.product_tab.load_products()  # ensure refresh
        self.product_tab.tkraise()

    def show_category_hierarchy(self):
        self.category_hierarchy.load_hierarchy()  # refresh
        self.category_hierarchy.tkraise()


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

        # Use a treeview without columns for hierarchy display
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_category)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=(5, 10), ipady=10, ipadx=5)

        ctk.CTkButton(button_frame, text="Add Category", command=self.add_category_popup).pack(side="left", padx=(10,5))
        ctk.CTkButton(button_frame, text="Edit Category", command=self.edit_category_popup).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Delete Category", fg_color="red", command=self.delete_category).pack(side="left", padx=(5,0))

        # load initial data
        self.load_categories()

    # ---------- HELPERS ----------
    def load_categories(self):
        """Reload category hierarchy from the database."""
        if not hasattr(self, 'tree'):
            return
        self.tree.delete(*self.tree.get_children())
        try:
            hierarchy = db.get_category_hierarchy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load categories: {e}")
            return

        def insert_node(parent_iid, node):
            iid = node['id']
            self.tree.insert(parent_iid, 'end', iid=iid, text=node['name'])
            for child in node.get('children', []):
                insert_node(iid, child)

        for root in hierarchy:
            insert_node('', root)

        for item in self.tree.get_children():
            self.tree.item(item, open=True)

    def on_select_category(self, event):
        pass

    def add_category_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Category")
        popup.geometry("320x260")

        ctk.CTkLabel(popup, text="Category Name:").pack(pady=(15,5))
        name_entry = ctk.CTkEntry(popup)
        name_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Parent Category:").pack(pady=(10,5))
        categories = db.get_all_categories()
        parent_options = ["None"] + [c['name'] for c in categories]
        parent_var = ctk.StringVar(value="None")
        parent_menu = ctk.CTkOptionMenu(popup, variable=parent_var, values=parent_options)
        parent_menu.pack(pady=5)

        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Missing Name", "Please enter a category name.")
                return
            parent_id = None
            selected_parent_name = parent_var.get()
            if selected_parent_name != "None":
                for c in categories:
                    if c['name'] == selected_parent_name:
                        parent_id = c['id']
                        break
            result = db.add_category(name, parent_id)
            if result.get('status') == 'error':
                messagebox.showerror("Error", result.get('message', 'Failed to add category.'))
            else:
                messagebox.showinfo("Success", result.get('message', 'Category added.'))
                popup.destroy()
                self.load_categories()
        ctk.CTkButton(popup, text="Save", command=save).pack(pady=15)

    def edit_category_popup(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a category to edit.")
            return
        # Fetch current data
        categories = db.get_all_categories()
        current = next((c for c in categories if str(c['id']) == str(selected)), None)
        if not current:
            messagebox.showerror("Error", "Selected category not found.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Edit Category")
        popup.geometry("340x280")

        ctk.CTkLabel(popup, text="New Name:").pack(pady=(15,5))
        name_entry = ctk.CTkEntry(popup)
        name_entry.insert(0, current['name'])
        name_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="New Parent:").pack(pady=(10,5))
        # Exclude self from parent choices
        parent_candidates = [c for c in categories if c['id'] != current['id']]
        parent_options = ["None"] + [c['name'] for c in parent_candidates]
        current_parent_name = "None"
        if current.get('parent_id'):
            parent_obj = next((c for c in categories if c['id'] == current['parent_id']), None)
            if parent_obj:
                current_parent_name = parent_obj['name']
        parent_var = ctk.StringVar(value=current_parent_name)
        parent_menu = ctk.CTkOptionMenu(popup, variable=parent_var, values=parent_options)
        parent_menu.pack(pady=5)

        def update():
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showwarning("Missing Name", "Please enter a new name.")
                return
            new_parent_id = None
            selected_parent_name = parent_var.get()
            if selected_parent_name != "None":
                for c in parent_candidates:
                    if c['name'] == selected_parent_name:
                        new_parent_id = c['id']
                        break
            result = db.update_category(current['id'], new_name=new_name, new_parent_id=new_parent_id)
            if result.get('status') == 'error':
                messagebox.showerror("Error", result.get('message', 'Failed to update category.'))
            else:
                messagebox.showinfo("Success", "Category updated.")
                popup.destroy()
                self.load_categories()
        ctk.CTkButton(popup, text="Update", command=update).pack(pady=15)

    def delete_category(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a category to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this category? This cannot be undone."):
            return
        try:
            result = db.delete_category(int(selected))
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
            return
        if result.get('status') == 'error':
            messagebox.showerror("Error", result.get('message', 'Delete failed.'))
        else:
            messagebox.showinfo("Success", "Category deleted.")
            self.load_categories()


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

    # ---------- HELPERS ----------
    def load_products(self):
        """Reload product data from the database."""
        if not hasattr(self, 'product_table'):
            return
        self.product_table.delete(*self.product_table.get_children())
        try:
            products = db.get_all_products()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {e}")
            return
        for p in products:
            self.product_table.insert('', 'end', iid=p['id'], values=(p['name'], p['price'], p['category_name'] or 'Uncategorized'))

    def add_product_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Product")
        popup.geometry("320x340")

        ctk.CTkLabel(popup, text="Product Name:").pack(pady=(15,5))
        name_entry = ctk.CTkEntry(popup)
        name_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Price:").pack(pady=(10,5))
        price_entry = ctk.CTkEntry(popup)
        price_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Category:").pack(pady=(10,5))
        categories = db.get_all_categories()
        cat_options = ["Uncategorized"] + [c['name'] for c in categories]
        cat_var = ctk.StringVar(value=cat_options[0])
        cat_menu = ctk.CTkOptionMenu(popup, variable=cat_var, values=cat_options)
        cat_menu.pack(pady=5)

        def save():
            name = name_entry.get().strip()
            price_raw = price_entry.get().strip()
            if not name or not price_raw:
                messagebox.showwarning("Missing Info", "Please fill all fields.")
                return
            try:
                price = float(price_raw)
            except ValueError:
                messagebox.showerror("Invalid Price", "Enter a valid number for price.")
                return
            category_id = None
            selected_cat = cat_var.get()
            if selected_cat != "Uncategorized":
                for c in categories:
                    if c['name'] == selected_cat:
                        category_id = c['id']
                        break
            result = db.add_product(name, price, category_id)
            if result.get('status') == 'error':
                messagebox.showerror("Error", result.get('message', 'Failed to add product.'))
            else:
                messagebox.showinfo("Success", "Product added.")
                popup.destroy()
                self.load_products()
        ctk.CTkButton(popup, text="Save", command=save).pack(pady=15)

    def edit_product_popup(self):
        selected = self.product_table.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a product to edit.")
            return
        data = self.product_table.item(selected, 'values')
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Product")
        popup.geometry("320x360")

        ctk.CTkLabel(popup, text="Product Name:").pack(pady=(15,5))
        name_entry = ctk.CTkEntry(popup)
        name_entry.insert(0, data[0])
        name_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Price:").pack(pady=(10,5))
        price_entry = ctk.CTkEntry(popup)
        price_entry.insert(0, data[1])
        price_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Category:").pack(pady=(10,5))
        categories = db.get_all_categories()
        cat_options = ["Uncategorized"] + [c['name'] for c in categories]
        current_cat_name = data[2] if data[2] else "Uncategorized"
        cat_var = ctk.StringVar(value=current_cat_name)
        cat_menu = ctk.CTkOptionMenu(popup, variable=cat_var, values=cat_options)
        cat_menu.pack(pady=5)

        def update():
            name = name_entry.get().strip()
            price_raw = price_entry.get().strip()
            if not name or not price_raw:
                messagebox.showwarning("Missing Info", "Please fill all fields.")
                return
            try:
                price = float(price_raw)
            except ValueError:
                messagebox.showerror("Invalid Price", "Enter a valid number for price.")
                return
            category_id = None
            selected_cat = cat_var.get()
            if selected_cat != "Uncategorized":
                for c in categories:
                    if c['name'] == selected_cat:
                        category_id = c['id']
                        break
            result = db.update_product(int(selected), name, price, category_id)
            if result.get('status') == 'error':
                messagebox.showerror("Error", result.get('message', 'Failed to update product.'))
            else:
                messagebox.showinfo("Success", "Product updated.")
                popup.destroy()
                self.load_products()
        ctk.CTkButton(popup, text="Update", command=update).pack(pady=15)

    def delete_product(self):
        selected = self.product_table.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a product to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete selected product? This cannot be undone."):
            return
        result = db.delete_product(int(selected))
        if result.get('status') == 'error':
            messagebox.showerror("Error", result.get('message', 'Delete failed.'))
        else:
            messagebox.showinfo("Success", "Product deleted.")
            self.load_products()


class CategoryHierarchyTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        ctk.CTkLabel(self, text="Category Hierarchy", font=("Arial", 20, "bold")).pack(pady=10)

        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Treeview with only Name and Price
        self.tree = ttk.Treeview(tree_frame, columns=("price",), show="tree headings")
        self.tree.heading("#0", text="Category & Product Name")
        self.tree.heading("price", text="Price (₱)")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.load_hierarchy()

    def load_hierarchy(self):
        self.tree.delete(*self.tree.get_children())

        categories = db.get_category_hierarchy()
        products = db.get_all_products()

        def insert_category(parent_iid, category_node):
            cat_iid = f"cat_{category_node['id']}"
            self.tree.insert(parent_iid, "end", iid=cat_iid, text=category_node['name'], values=("",))

            # Insert products under this category
            for p in products:
                if p['category_id'] == category_node['id']:
                    prod_iid = f"prod_{p['id']}"
                    self.tree.insert(cat_iid, "end", iid=prod_iid, text=p['name'], values=(f"{p['price']:.2f}",))

            # Insert subcategories recursively
            for child in category_node.get("children", []):
                insert_category(cat_iid, child)

        for root in categories:
            insert_category("", root)

        # Expand all
        for item in self.tree.get_children():
            self.tree.item(item, open=True)


App('Class based app with ctk', (900, 600))
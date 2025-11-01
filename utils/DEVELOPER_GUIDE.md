# Developer Role Guide

This guide explains our project's structure and *your* specific job. We have divided the project into two main parts:

1.  **The Engine (Database Logic)**
2.  **The Dashboard (UI/Menu Logic)**

You must **only** work in the files assigned to your role.

---

## Role 1: Database Developer (The "Engine"️)

Your mission is to handle all data and database logic. You make sure data can be saved, fetched, updated, and deleted.

### Files You OWN:

* `models/category.py`
* `models/product.py`
* `database/db_manager.py`

### Your Tasks:

1.  **Define Models:**
    * In **`models/category.py`**, define the `Category` class.
    * In **`models/product.py`**, define the `Product` class.
2.  **Build the Database:**
    * In **`database/db_manager.py`**, write the function that creates the `.db` file and the `categories` and `products` tables.
3.  **Write CRUD Functions:**
    * In **`database/db_manager.py`**, write all the functions the app needs, such as:
        * `add_category(name)`
        * `get_all_categories()`
        * `update_product(product_id, new_name, new_price)`
        * `delete_product(product_id)`
        * ...and so on.

### Files You MUST NOT Edit:

* Do **NOT** edit `ui/menu.py` or `main.py`.
* You should **NEVER** use `print()` or `input()` in your files. Your functions should only `return` data (e.g., `return all_products_list`).

---

## Role 2: UI/Menu Developer (The "Dashboard" )

Your mission is to build the user interface. You handle everything the user sees (`print`) and types (`input`).

### Files You OWN:

* `ui/menu.py`
* `utils/validators.py`

### Your Tasks:

1.  **Build Menus:**
    * In **`ui/menu.py`**, write functions that `print` the menus, like:
        * `show_main_menu()`
        * `show_product_menu()`
        * `show_success_message(message)`
2.  **Get User Input:**
    * In **`ui/menu.py`**, write functions that ask the user for information, like:
        * `get_menu_choice()`
        * `get_new_product_details()` (This should ask for name, price, etc., and `return` them)
3.  **Validate Input:**
    * In **`utils/validators.py`**, create helper functions to check user input, like:
        * `is_not_empty(text)`
        * `is_valid_price(price)`

### Files You MUST NOT Edit:

* Do **NOT** edit `database/db_manager.py`, `models/`, or `main.py`.
* You should **NEVER** write any SQL code. Your job is to *get* data from the user and *give* it to `main.py`.
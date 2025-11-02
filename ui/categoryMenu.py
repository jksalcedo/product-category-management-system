from utils.validator import *

def add_category():
    while True:
        category_name = input("Enter Category Name: ")
        if not is_not_empty(category_name):
            print("Category Name cannot be empty.")
            continue

        # Add logic to save category to data source
        print(f"Category '{category_name}' added successfully!")
        break

def view_categories():
    categories = []
    if not categories:
        print("No Categories Available.")
        return

    # To change on Final code
    print("\n~~~~~~ Category Lists ~~~~~~")
    for category in categories:
        print(f"ID:   {category['id']}")
        print(f"Name: {category['name']}")

def update_category():
    pass

def delete_category():
    pass

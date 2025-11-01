from utils.validator import *


def add_product():
    while True:
        name = input("Enter Product Name: ")
        if not is_not_empty(name):
            print("Product Name cannot be empty.")
            continue

        price = input("Enter product Price: ")
        if not is_not_empty(price):
            print("Product Price cannot be empty.")
            continue

        category = input("Enter product Category ID: ")
        if not is_not_empty(category):
            print("Product Category ID cannot be empty.")
            continue

        # Add logic to save product to data source
        print(f"Product '{name}' added successfully!")

def view_products():
    products = []        # Input product list from data source
    if not products:
        print("No products Available.")
        return

    # To change on Final code
    print("\n~~~~~~ Product Lists ~~~~~~")
    for product in products:
        print(f"ID:    {product['id']}")
        print(f"Name:  {product['name']}")
        print(f"Price: {product['price']}")


def update_products():

    pass

def delete_products():
    pass

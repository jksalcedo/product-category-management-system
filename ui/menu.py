
def main():
    while True:
        print("\n~~~~~  Main Menu  ~~~~~")
        print("1. Manage Products")
        print("2. Manage Categories")
        print("0. Exit")
        choice = int(input("\nSelect an Option: "))

        match choice:
            case 1:
                show_product_menu()
            case 2:
                show_category_menu()
            case 0:
                print("Exiting the program...")
                break
            case _:
                print("Invalid choice. Please try again.")


def show_product_menu():
    while True:
        print("\n~~~~~  Product Menu  ~~~~~")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("0. Back to Main Menu")
        choice = int(input("\nSelect an Option: "))

        match choice:
            case 1:
                print("Add Product...")
            case 2:
                print("View Products...")
            case 3:
                print("Update Product...")
            case 4:
                print("Delete Product...")
            case 0:
                print("Returning to Main Menu...")
                break
            case _:
                print("Invalid choice. Please try again.")


def show_category_menu():
    while True:
        print("\n~~~~~  Category Menu  ~~~~~")
        print("1. Add Category")
        print("2. View Categories")
        print("3. Update Category")
        print("4. Delete Category")
        print("0. Back to Main Menu")
        choice = int(input("\nSelect an Option: "))

        match choice:
            case 1:
                print("Add Category...")
            case 2:
                print("View Categories...")
            case 3:
                print("Update Category...")
            case 4:
                print("Delete Category...")
            case 0:
                print("Returning to Main Menu...")
                break
            case _:
                print("Invalid choice. Please try again.")


main()
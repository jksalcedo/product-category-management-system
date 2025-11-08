import sqlite3
from models.category import Category
from models.product import Product

DB_NAME = "inventory.db"

# DATABASE INITIALIZATION

def _column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cursor.fetchall()]
    return column in cols

def initialize_database():
    """Create database and tables if not existing and ensure schema matches hierarchy needs."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Categories now support hierarchy via parent_id
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES categories(id)
        )
        """
    )

    # If table already existed without parent_id, add it
    if not _column_exists(cursor, "categories", "parent_id"):
        cursor.execute("ALTER TABLE categories ADD COLUMN parent_id INTEGER")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
        """
    )

    conn.commit()
    conn.close()
    return True

# CATEGORY

def add_category(name, parent_id=None):
    """Insert a new category or subcategory.
    parent_id: optional existing category id to attach as parent
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # Validate parent if provided
        if parent_id is not None:
            cursor.execute("SELECT id FROM categories WHERE id = ?", (parent_id,))
            if cursor.fetchone() is None:
                conn.close()
                return {"status": "error", "message": "Parent category not found."}
        cursor.execute("INSERT INTO categories (name, parent_id) VALUES (?, ?)", (name, parent_id))
        conn.commit()
        result = {"status": "success", "message": f"Category '{name}' added.", "id": cursor.lastrowid}
    except sqlite3.IntegrityError:
        result = {"status": "error", "message": "Category already exists."}
    conn.close()
    return result


def get_all_categories():
    """Retrieve all categories with parent info."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, parent_id FROM categories")
    rows = cursor.fetchall()
    conn.close()
    return [Category(id=row[0], name=row[1], parent_id=row[2]).to_dict() for row in rows]


def update_category(category_id, new_name=None, new_parent_id=None):
    """Update a category name and/or parent.
    If a field is None it won't be updated.
    Prevent setting parent to self or creating cycles.
    """
    if new_name is None and new_parent_id is None:
        return {"status": "error", "message": "Nothing to update."}

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # If updating parent, validate
    if new_parent_id is not None:
        if new_parent_id == category_id:
            conn.close()
            return {"status": "error", "message": "Category cannot be its own parent."}
        cursor.execute("SELECT id FROM categories WHERE id = ?", (new_parent_id,))
        if cursor.fetchone() is None:
            conn.close()
            return {"status": "error", "message": "Parent category not found."}
        # Basic cycle prevention: ensure new parent isn't a descendant of this category
        def _is_descendant(cur, ancestor_id, possible_descendant_id):
            cur.execute("SELECT id FROM categories WHERE parent_id = ?", (ancestor_id,))
            children = [r[0] for r in cur.fetchall()]
            if not children:
                return False
            if possible_descendant_id in children:
                return True
            for ch in children:
                if _is_descendant(cur, ch, possible_descendant_id):
                    return True
            return False
        if _is_descendant(cursor, category_id, new_parent_id):
            conn.close()
            return {"status": "error", "message": "Cannot set a descendant as parent (cycle)."}

    sets = []
    params = []
    if new_name is not None:
        sets.append("name = ?")
        params.append(new_name)
    if new_parent_id is not None:
        sets.append("parent_id = ?")
        params.append(new_parent_id)
    params.append(category_id)

    cursor.execute(f"UPDATE categories SET {', '.join(sets)} WHERE id = ?", tuple(params))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return {"status": "success" if updated else "error", "updated": updated}


def delete_category(category_id):
    """Delete a category only if it has no products and no subcategories."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products WHERE category_id = ?", (category_id,))
    product_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM categories WHERE parent_id = ?", (category_id,))
    child_count = cursor.fetchone()[0]

    if product_count > 0:
        conn.close()
        return {"status": "error", "message": "Category has existing products."}
    if child_count > 0:
        conn.close()
        return {"status": "error", "message": "Category has subcategories."}

    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return {"status": "success" if deleted else "error", "deleted": deleted}

# Tree helpers

def get_subcategories(parent_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, parent_id FROM categories WHERE parent_id = ?", (parent_id,))
    rows = cursor.fetchall()
    conn.close()
    return [Category(id=r[0], name=r[1], parent_id=r[2]).to_dict() for r in rows]


def get_parent_category(category_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT c2.id, c2.name, c2.parent_id FROM categories c1 LEFT JOIN categories c2 ON c1.parent_id = c2.id WHERE c1.id = ?", (category_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None or row[0] is None:
        return None
    return Category(id=row[0], name=row[1], parent_id=row[2]).to_dict()


def get_category_hierarchy():
    """Return the entire category hierarchy as a nested structure.
    Each node: {id, name, parent_id, children: [...]}"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, parent_id FROM categories")
    rows = cursor.fetchall()
    conn.close()

    nodes = {r[0]: {"id": r[0], "name": r[1], "parent_id": r[2], "children": []} for r in rows}
    roots = []
    for nid, node in nodes.items():
        pid = node["parent_id"]
        if pid and pid in nodes:
            nodes[pid]["children"].append(node)
        else:
            roots.append(node)
    return roots

# PRODUCT

def add_product(name, price, category_id):
    """Insert a new product."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, category_id) VALUES (?, ?, ?)",
        (name, price, category_id)
    )
    conn.commit()
    pid = cursor.lastrowid
    conn.close()
    return {"status": "success", "product_id": pid}


def get_all_products():
    """Retrieve all products with category names."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.id, p.name, p.price, p.category_id, c.name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        """
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "category_id": row[3],
            "category_name": row[4],
        }
        for row in rows
    ]


def update_product(product_id, new_name, new_price, new_category_id):
    """Update product details."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE products
        SET name = ?, price = ?, category_id = ?
        WHERE id = ?
        """,
        (new_name, new_price, new_category_id, product_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return {"status": "success" if updated else "error", "updated": updated}


def delete_product(product_id):
    """Delete a product by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return {"status": "success" if deleted else "error", "deleted": deleted}
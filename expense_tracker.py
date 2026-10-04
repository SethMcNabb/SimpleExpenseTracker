import sqlite3

DB_FILE = "finance.db"


def get_connection():
    """Connect to SQLite and enforce foreign key constraints."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Initialize tables from schema.sql and seed baseline categories if empty."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Check if the categories table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories';")
        if not cursor.fetchone():
            with open("schema.sql", "r") as file:
                conn.executescript(file.read())
            
            # Seed default categories so foreign keys have valid parents immediately
            cursor.execute("INSERT INTO categories (name) VALUES ('Groceries'), ('Utilities'), ('Entertainment');")
            conn.commit()


def add_category():
    """CREATE: Adds a new expense category."""
    name = input("Enter new category name: ").strip()
    if not name:
        print("Category name cannot be empty.")
        return

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categories (name) VALUES (?);", (name,))
            conn.commit()
            print(f"Category '{name}' created successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: Category '{name}' already exists.")


def add_transaction():
    """CREATE: Inserts a new transaction referencing a category foreign key."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category_id, name FROM categories;")
        categories = cursor.fetchall()

    if not categories:
        print("No categories found. Please add a category first.")
        return

    print("\nAvailable Categories:")
    for cat_id, cat_name in categories:
        print(f"  [{cat_id}] {cat_name}")

    try:
        category_id = int(input("Select Category ID: "))
        amount = float(input("Enter amount ($): "))
        description = input("Enter description/memo: ").strip()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transactions (category_id, amount, description) VALUES (?, ?, ?);",
                (category_id, amount, description),
            )
            conn.commit()
            print("Transaction recorded successfully.")
    except ValueError:
        print("Error: Amount and Category ID must be valid numbers.")
    except sqlite3.IntegrityError as err:
        print(f"Foreign Key Error: Invalid Category ID selected ({err}).")


def view_transactions():
    """READ (MULTI-TABLE JOIN): Displays transactions joined with their category names."""
    query = """
        SELECT 
            t.transaction_id,
            c.name AS category_name,
            t.amount,
            t.description
        FROM transactions t
        INNER JOIN categories c ON t.category_id = c.category_id
        ORDER BY t.transaction_id DESC;
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    print("\n--- ALL TRANSACTIONS (JOIN) ---")
    if not rows:
        print("No transactions logged yet.")
        return

    print(f"{'ID':<4} | {'Category':<15} | {'Amount':<9} | {'Description'}")
    print("-" * 50)
    for t_id, cat, amt, desc in rows:
        print(f"{t_id:<4} | {cat:<15} | ${amt:<8.2f} | {desc or ''}")


def view_category_summary():
    """READ (AGGREGATE): Calculates total spending per category using GROUP BY."""
    query = """
        SELECT 
            c.name,
            COALESCE(SUM(t.amount), 0.0) AS total_spent
        FROM categories c
        LEFT JOIN transactions t ON c.category_id = t.category_id
        GROUP BY c.category_id
        ORDER BY total_spent DESC;
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    print("\n--- SPENDING BY CATEGORY (GROUP BY) ---")
    print(f"{'Category':<15} | {'Total Spent'}")
    print("-" * 30)
    for cat, total in rows:
        print(f"{cat:<15} | ${total:.2f}")


def update_transaction():
    """UPDATE: Modifies amount and description of an existing transaction."""
    view_transactions()
    try:
        t_id = int(input("\nEnter Transaction ID to update: "))
        new_amt = float(input("Enter new amount ($): "))
        new_desc = input("Enter new description: ").strip()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE transactions SET amount = ?, description = ? WHERE transaction_id = ?;",
                (new_amt, new_desc, t_id),
            )
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Transaction #{t_id} updated successfully.")
            else:
                print(f"No transaction found with ID #{t_id}.")
    except ValueError:
        print("Error: Invalid numeric input.")


def delete_transaction():
    """DELETE: Removes a transaction by its primary key ID."""
    view_transactions()
    try:
        t_id = int(input("\nEnter Transaction ID to delete: "))
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE transaction_id = ?;", (t_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Transaction #{t_id} deleted successfully.")
            else:
                print(f"No transaction found with ID #{t_id}.")
    except ValueError:
        print("Error: Invalid ID.")


def display_menu():
    """CLI Menu Loop."""
    while True:
        print("\n" + "=" * 35)
        print("     PERSONAL EXPENSE TRACKER")
        print("=" * 35)
        print("1. View Transactions (JOIN)")
        print("2. Category Spending Summary (GROUP BY)")
        print("3. Record New Transaction (CREATE)")
        print("4. Add New Category (CREATE)")
        print("5. Update Transaction (UPDATE)")
        print("6. Delete Transaction (DELETE)")
        print("7. Exit")
        print("-" * 35)

        choice = input("Select an option (1-7): ").strip()
        if choice == "1":
            view_transactions()
        elif choice == "2":
            view_category_summary()
        elif choice == "3":
            add_transaction()
        elif choice == "4":
            add_category()
        elif choice == "5":
            update_transaction()
        elif choice == "6":
            delete_transaction()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 7.")


if __name__ == "__main__":
    init_db()
    display_menu()
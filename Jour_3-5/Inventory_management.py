####SQL####
# CREATE DATABASE store;

# CREATE TABLE category (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL
# );

# CREATE TABLE product (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     description TEXT,
#     price INT,
#     quantity INT,
#     id_category INT,
#     FOREIGN KEY (id_category) REFERENCES category(id)    ###A foreign key that links the product to a category.###
# );

####Python####
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, messagebox

load_dotenv()
PASSWORD = os.getenv("PASSWORD")

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=PASSWORD,
        use_pure=True,
        database="store"
    )

# This function inserts a new category into the category table.
def add_category(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO category (name) VALUES (%s)", (name,))
    conn.commit()
    cursor.close()
    conn.close()

# This function inserts a new product into the product table.
def add_product(name, description, price, quantity, id_category):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)",
                   (name, description, price, quantity, id_category))
    conn.commit()
    cursor.close()
    conn.close()

# This function retrieves all products from the product table.
def get_all_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products


# This function updates the information of an existing product.
def update_product(product_id, name, description, price, quantity, id_category):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE product SET name=%s, description=%s, price=%s, quantity=%s, id_category=%s WHERE id=%s",
                   (name, description, price, quantity, id_category, product_id))
    conn.commit()
    cursor.close()
    conn.close()

# This function removes a product from the product table.
def delete_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM product WHERE id=%s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
# This function updates the table with the current products.
def refresh_products():
    for row in tree.get_children():
        tree.delete(row)
    products = get_all_products()
    for product in products:
        tree.insert("", "end", values=product)


# This function opens a new window to add a product.
def add_product_window():
    def save_product():
        name = entry_name.get()
        description = entry_description.get()
        price = int(entry_price.get())
        quantity = int(entry_quantity.get())
        id_category = int(entry_category.get())
        add_product(name, description, price, quantity, id_category)
        messagebox.showinfo("Success", "Product added successfully")
        refresh_products()
        add_window.destroy()

    add_window = tk.Toplevel()
    add_window.title("Add Product")

    tk.Label(add_window, text="Name").grid(row=0, column=0)
    entry_name = tk.Entry(add_window)
    entry_name.grid(row=0, column=1)

    tk.Label(add_window, text="Description").grid(row=1, column=0)
    entry_description = tk.Entry(add_window)
    entry_description.grid(row=1, column=1)    

    tk.Label(add_window, text="Price").grid(row=2, column=0)
    entry_price = tk.Entry(add_window)
    entry_price.grid(row=2, column=1)

    tk.Label(add_window, text="Quantity").grid(row=3, column=0)
    entry_quantity = tk.Entry(add_window)
    entry_quantity.grid(row=3, column=1)

    tk.Label(add_window, text="Category ID").grid(row=4, column=0)
    entry_category = tk.Entry(add_window)
    entry_category.grid(row=4, column=1)

    tk.Button(add_window, text="Save", command=save_product).grid(row=5, column=0, columnspan=2)


# This function deletes the selected product from the table.
def delete_product_window():
    selected_item = tree.selection()[0]
    product_id = tree.item(selected_item, 'values')[0]
    delete_product(product_id)
    refresh_products()

root = tk.Tk()
root.title("Stock Management")

tree = ttk.Treeview(root, columns=("ID", "Name", "Description", "Price", "Quantity", "Category ID"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Description", text="Description")
tree.heading("Price", text="Price")
tree.heading("Quantity", text="Quantity")
tree.heading("Category ID", text="Category ID")
tree.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Product", command=add_product_window)
add_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Delete Product", command=delete_product_window)
delete_button.pack(side=tk.LEFT, padx=5)

refresh_products()
root.mainloop()
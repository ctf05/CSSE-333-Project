import tkinter as tk
from tkinter import ttk
import pyodbc



def connect(server, database, username, password):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return conn

conn = connect("titan.csse.rose-hulman.edu", "OneProduct", "SodaBaseUserbeadlich", "Password123")
conn.autocommit = True
cursor = conn.cursor()
global tree
global combobox
global entry1
global entry2
global entry3
global entry4
global entry5
global entry6

def add_clicked():
    try:
        cursor.execute("EXEC dbo.addCustomer @FName = ?, @LName = ?, @Phone = ?, @Address = ?, @BillingID = ?", (entry1.get(), entry2.get(), entry3.get(), entry4.get(), None))
    except:
        print("error")

def update_clicked():
    try:
        cursor.execute("EXEC dbo.UpdateCustomer @ID = ?, @FName = ?, @LName = ?, @Phone = ?, @Address = ?, @BillingID = ?", (entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), None))
    except:
        print("error")

def delete_clicked():
    try:
        cursor.execute("EXEC dbo.DeleteCustomer @ID = ?", (entry1.get()))
    except:
        print("error")

def view_clicked():
    print(combobox.get())
    if combobox.get() == "Application":
        cursor.execute("""
        SELECT *
        FROM Application""")
        print(cursor.fetchall())
    elif combobox.get() == "Customer":
        cursor.execute("""
        SELECT *
        FROM Customer""")
    elif combobox.get() == "BillingInfo":
        cursor.execute("""
        SELECT *
        FROM BillingInfo""")
    elif combobox.get() == "Category":
        cursor.execute("""
        SELECT *
        FROM Category""")
    elif combobox.get() == "onOrder":
        cursor.execute("""
        SELECT *
        FROM onOrder""")
    elif combobox.get() == "Order":
        cursor.execute("""
        SELECT *
        FROM Order""")
    elif combobox.get() == "Product":
        cursor.execute("""
        SELECT *
        FROM Product""")
    elif combobox.get() == "Review":
        cursor.execute("""
        SELECT *
        FROM Review""")
    elif combobox.get() == "Supplier":
        cursor.execute("""
        SELECT *
        FROM Supplier""")
    insert_data(cursor.fetchall())


def insert_data(data_list):
    for item in table.get_children():
        table.delete(item)
    for row in data_list:
        table.insert("", tk.END, values=row)

def login_success():
    root = tk.Tk()
    root.geometry("1250x500")
    root.title("Admin Control Panel")

    # Create a dropdown menu
    global combobox
    combobox_label = ttk.Label(root, text="Select a table:")
    combobox_label.grid(row=0, column=0, padx=10, pady=10)
    combobox = ttk.Combobox(root, values=["Application", "BillingInfo", "Category", "Customer", "onOrder", "Order", "Product", "Review", "Supplier"])
    combobox.current(0)
    combobox.grid(row=0, column=1, padx=10, pady=10)
    global entry1
    global entry2
    global entry3
    global entry4
    global entry5
    global entry6
    # Create six textboxes
    entry1 = ttk.Entry(root)
    entry1.grid(row=1, column=0, padx=5, pady=10)
    entry2 = ttk.Entry(root)
    entry2.grid(row=1, column=1, padx=5, pady=10)
    entry3 = ttk.Entry(root)
    entry3.grid(row=1, column=2, padx=5, pady=10)
    entry4 = ttk.Entry(root)
    entry4.grid(row=1, column=3, padx=5, pady=10)
    entry5 = ttk.Entry(root)
    entry5.grid(row=1, column=4, padx=5, pady=10)
    entry6 = ttk.Entry(root)
    entry6.grid(row=1, column=5, padx=5, pady=10)

    # Create four buttons
    button1 = ttk.Button(root, text="Add", command=add_clicked)
    button1.grid(row=3, column=0, padx=7, pady=10)
    button2 = ttk.Button(root, text="Update", command=update_clicked)
    button2.grid(row=3, column=1, padx=7, pady=10)
    button3 = ttk.Button(root, text="Delete", command=delete_clicked)
    button3.grid(row=3, column=2, padx=7, pady=10)
    button4 = ttk.Button(root, text="View", command=view_clicked)
    button4.grid(row=3, column=3, padx=7, pady=10)


    # Create a table to display data
    global table
    table = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5", "col6"), show='headings')
    table.heading("col1", text="Column 1")
    table.heading("col2", text="Column 2")
    table.heading("col3", text="Column 3")
    table.heading("col4", text="Column 4")
    table.heading("col5", text="Column 5")
    table.heading("col6", text="Column 6")
    table.grid(row=4, column=0, columnspan=6, padx=10, pady=10)
    pass

def login_failure():
    # code to run if login fails
    pass

def check_credentials():
    # check if the entered username and password match
    # the expected values  

    if username_entry.get() == 'admin' and password_entry.get() == 'password':
        login_success()
        root.destroy()
    elif username_entry.get() == 'home' and password_entry.get() == 'page':
        home_page()
        root.destroy()
    else:
        login_failure()

def home_page():
    root = tk.Tk()
    root.title("Home Page")
    root.geometry("1250x500")

    label = tk.Label(root, text="Welcome to One Product", font=("TkDefaultFont", 16))
    label.pack()

    cursor.execute("""Select * From Product Where ForSale = 1""")
    products = cursor.fetchall()
    
    listbox = tk.Listbox(root, width=100)
    for product in products:
        listbox.insert(tk.END, product)
    listbox.pack()    

    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack()

def application_page():
    form = tk.Toplevel(root)
    form.title("Submit Product Application")
    form.geometry("1250x500")
    form_label = tk.Label(form, text="Submit Product Application", font=("TkDefaultFont", 16))
    form_label.pack()

def view_product_page():
    pass   

root = tk.Tk()
root.title("Login")

username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0)

username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)

password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1)

login_button = tk.Button(root, text="Login", command=check_credentials)
login_button.grid(row=2, column=0, columnspan=2)

add_product_button = tk.Button(root, text="Submit Product Application", command=application_page)
add_product_button.grid(row=3, column=0, columnspan=2)

root.mainloop()


def execute_stored_procedure(conn):
    #connect to the SQL Server instance

    # call the stored procedure and pass the values of the dropdown menus as parameters
    ##cursor.execute("{CALL dbo.addCustomer (?,?,?,?,?)}", ("fname", "lname", "123-545-3443", "jonesville", None))
    cursor.execute("{CALL dbo.addCustomer ('re','ree','123-454-3232','jone',null)}")
    # retrieve the results of the stored procedure
    #results = cursor.fetchall()
    # close the connection to the SQL Server instance
    cursor.close()
    conn.close()
    #return results



import tkinter as tk
from tkinter import ttk
import pyodbc

def main():
    execute_stored_procedure(conn)


def connect(server, database, username, password):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return conn

conn = connect("titan.csse.rose-hulman.edu", "OneProduct", "SodaBaseUserbeadlich", "Password123")
cursor = conn.cursor()

def check_credentials():
    # check if the entered username and password match
    # the expected values
    if username_entry.get() == 'admin' and password_entry.get() == 'password':
        login_success()
    else:
        login_failure()

def login_success():
    # code to run if login is successful
    pass

def login_failure():
    # code to run if login fails
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

def show_selected():
    print("Selected option:", combobox.get())

def add_clicked():
    print("Button 1 clicked")

def update_clicked():
    print("Button 2 clicked")

def delete_clicked():
    print("Button 3 clicked")

def view_clicked():
    print("Button 4 clicked")

def insert_data():
    data_list.append([entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get()])
    for i in range(len(data_list)):
        for j in range(10):
            table.set(i, j, data_list[i][j])
    print(data_list)

root = tk.Tk()
root.geometry("1250x500")
root.title("Admin Control Panel")

# Create a dropdown menu
combobox_label = ttk.Label(root, text="Select a table:")
combobox_label.grid(row=0, column=0, padx=10, pady=10)
combobox = ttk.Combobox(root, values=["Application", "BillingInfo", "Category", "Customer", "onOrder", "Order", "Product", "Review", "Supplier"])
combobox.current(0)
combobox.grid(row=0, column=1, padx=10, pady=10)

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

table = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5", "col6"), show='headings')
table.heading("col1", text="Column 1")
table.heading("col2", text="Column 2")
table.heading("col3", text="Column 3")
table.heading("col4", text="Column 4")
table.heading("col5", text="Column 5")
table.heading("col6", text="Column 6")
table.grid(row=4, column=0, columnspan=6, padx=10, pady=10)



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

cursor.execute("""
    SELECT *
    FROM Application""")
print(cursor.fetchall())
# retrieve the results of the stored procedure
#results = cursor.fetchall()
main()
root.mainloop()

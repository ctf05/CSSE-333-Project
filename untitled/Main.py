import tkinter as tk
from tkinter import ttk

import bcrypt as bcrypt
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
global username_entry
global password_entry
global first_name_entry
global last_name_entry
global address_entry
global phone_entry
global card_entry
global expiration_entry
global security_entry
global card_type_entry

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
    global password_entry

    if username_entry.get() == "admin" and password_entry.get() == "password":
        login_success()
        return

    password = password_entry.get().encode()

    cursor.execute("""
        SELECT PasswordSalt
        FROM Login
        WHERE Username = ?""",(username_entry.get()))
    try:
        password_salt = cursor.fetchone()[0].encode()
    except:
        print("Username not found")
        login_failure()

    password_hash = bcrypt.hashpw(password, password_salt)

    cursor.execute("""
        SELECT *
        FROM Login
        WHERE PasswordHash = ?""",(password_hash.decode()[0:49]))
    try:
        print(password_hash.decode()[0:49])
        user = cursor.fetchone()
        print(user)
        print(user[1])
        home_page(user[1])
    except:
        print("Password incorrect")
        login_failure()


def home_page(cid):
    root = tk.Tk()
    root.title("Home Page")
    root.geometry("1250x500")

    def go_to_product(event):
        cs = listbox.curselection()
        print(products[cs[0]])
        open_product_page(products[cs[0]][0])

    label = tk.Label(root, text="Welcome to One Product", font=("TkDefaultFont", 16))
    label.pack()

    cursor.execute("""Select * From Product Where ForSale = 1""")
    products = cursor.fetchall()
    
    listbox = tk.Listbox(root, width=100)
    for product in products:
        listbox.insert(tk.END, product)
    listbox.bind("<Double-1>", go_to_product)
    listbox.pack()

    def view_cart_page():
        cart_page(cid)

    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack()

    cart_button = tk.Button(root, text="View Cart", command=view_cart_page)
    cart_button.pack()

def open_product_page(productID):
    product_page = tk.Tk()
    product_page.title("Product Details")
    product_page.geometry("1250x500")

    label = tk.Label(product_page, text="Product Details", font=("TkDefaultFont", 16))
    label.pack()

    cursor.execute("""Select * From Product Where ProductID = ?""", productID)
    product = cursor.fetchall()[0]
    print(product)

    product_name_label = tk.Label(product_page, text="Product Name: ")
    product_name_label.pack()
    product_name_display = tk.Label(product_page, text=product[1])
    product_name_display.pack()

    product_company_label = tk.Label(product_page, text="Company: ")
    product_company_label.pack()
    product_company_display = tk.Label(product_page, text=product[2])
    product_company_display.pack()

    product_category_label = tk.Label(product_page, text="Category: ")
    product_category_label.pack()
    product_category_display = tk.Label(product_page, text=product[3])
    product_category_display.pack()

    product_price_label = tk.Label(product_page, text="Price: ")
    product_price_label.pack()
    product_price_display = tk.Label(product_page, text=product[4])
    product_price_display.pack()

    product_description_label = tk.Label(product_page, text="Description: ")
    product_description_label.pack()
    product_description_display = tk.Label(product_page, text=product[9])
    product_description_display.pack()

    def on_back_click():
        product_page.destroy()

    back_button = tk.Button(product_page, text="Back", command=on_back_click)
    back_button.pack()

def submit_application(product_name, product_company, product_category, product_price, product_description,  product_company_phone, product_company_website):
    cursor.execute("""EXEC dbo.SubmitProductApplication @PName = ?, @CatName = ?, @SName = ?, @PDesc = ?, @ProPrice = ?, @SPhone = ?, @SWebsite = ?""", 
    (product_name, product_category, product_company, product_description, product_price, product_company_phone, product_company_website))

def registration_page():
    root = tk.Tk()
    root.geometry("1250x500")
    root.title("Registration Page")
    global username_entry
    global password_entry
    global first_name_entry
    global last_name_entry
    global address_entry
    global phone_entry
    global card_entry
    global expiration_entry
    global security_entry
    global card_type_entry
    global username_label
    global password_label
    global first_name_label
    global last_name_label
    global address_label
    global phone_label
    global card_label
    global expiration_label
    global security_label
    global card_type_label
    # Create a label for the username input box
    username_label = tk.Label(root, text="Username")
    username_label.grid(row=0, column=0, padx=10, pady=10)
    # Create an input box for the username
    username_entry = tk.Entry(root)
    username_entry.grid(row=0, column=1, padx=10, pady=10)
    # Create a label for the password input box
    password_label = tk.Label(root, text="Password")
    password_label.grid(row=1, column=0, padx=10, pady=10)
    # Create an input box for the password
    password_entry = tk.Entry(root)
    password_entry.grid(row=1, column=1, padx=10, pady=10)
    # Create a label for the first name input box
    first_name_label = tk.Label(root, text="First Name")
    first_name_label.grid(row=2, column=0, padx=10, pady=10)
    # Create an input box for the first name
    first_name_entry = tk.Entry(root)
    first_name_entry.grid(row=2, column=1, padx=10, pady=10)
    # Create a label for the last name input box
    last_name_label = tk.Label(root, text="Last Name")
    last_name_label.grid(row=3, column=0, padx=10, pady=10)
    # Create an input box for the last name
    last_name_entry = tk.Entry(root)
    last_name_entry.grid(row=3, column=1, padx=10, pady=10)
    # Create a label for the address input box
    address_label = tk.Label(root, text="Address")
    address_label.grid(row=4, column=0, padx=10, pady=10)
    # Create an input box for the address
    address_entry = tk.Entry(root)
    address_entry.grid(row=4, column=1, padx=10, pady=10)
    # Create a label for the phone number input box
    phone_label = tk.Label(root, text="Phone Number")
    phone_label.grid(row=5, column=0, padx=10, pady=10)
    # Create an input box for the phone number
    phone_entry = tk.Entry(root)
    phone_entry.grid(row=5, column=1, padx=10, pady=10)
    # Create a label for the card number input box
    card_label = tk.Label(root, text="Card Number")
    card_label.grid(row=6, column=0, padx=10, pady=10)
    # Create an input box for the card number
    card_entry = tk.Entry(root)
    card_entry.grid(row=6, column=1, padx=10, pady=10)
    # Create a label for the expiration date input box
    expiration_label = tk.Label(root, text="Expiration Date")
    expiration_label.grid(row=7, column=0, padx=10, pady=10)
    # Create an input box for the expiration date
    expiration_entry = tk.Entry(root)
    expiration_entry.grid(row=7, column=1, padx=10, pady=10)
    # Create a label for the security code input box
    security_label = tk.Label(root, text="Security Code")
    security_label.grid(row=8, column=0, padx=10, pady=10)
    # Create an input box for the security code
    security_entry = tk.Entry(root)
    security_entry.grid(row=8, column=1, padx=10, pady=10)
    # Create a label for the card type input box
    card_type_label = tk.Label(root, text="Card Type")
    card_type_label.grid(row=9, column=0, padx=10, pady=10)
    # Create a drop box for the card type
    card_type_entry = ttk.Combobox(root, values=["Debit", "Credit"])
    card_type_entry.grid(row=9, column=1, padx=10, pady=10)
    # Create a submit button
    submitRegister = tk.Button(root, text="Submit", command=SubmitRegister)
    submitRegister.grid(row=10,column=0)

def SubmitRegister():
    global username_entry
    global password_entry
    global first_name_entry
    global last_name_entry
    global address_entry
    global phone_entry
    global card_entry
    global expiration_entry
    global security_entry
    global card_type_entry
    # Get the username from the input box
    username = username_entry.get()
    # Get the password from the input box
    password = password_entry.get()
    # Get the first name from the input box
    first_name = first_name_entry.get()
    # Get the last name from the input box
    last_name = last_name_entry.get()
    # Get the address from the input box
    address = address_entry.get()
    # Get the phone number from the input box
    phone = phone_entry.get()
    # Get the card number from the input box
    card = card_entry.get()
    # Get the expiration date from the input box
    expiration = expiration_entry.get()
    # Get the security code from the input box
    security = security_entry.get()
    # Get the card type from the input box
    card_type = card_type_entry.get()

    # Hash the password
    password_salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf8'), password_salt)

    try:
        cursor.execute("EXEC dbo.RegisterUser @UserName = ?, @PasswordSalt = ?, @PasswordHash = ?, @Address = ?, "
                       "@FName = ?, @LName = ?, @Phone = ?, @CardType = ?, @CardNumber = ?, @ExperationDate = ?, @SecurityCode = ?",
                       (username, password_salt.decode(), password_hash.decode()[0:49], address, first_name, last_name, phone, card_type,
                        card, expiration, security))
    except:
        print("error")

def application_page():
    root = tk.Tk()
    root.title("Submit Product Application")
    root.geometry("1250x500")

    label = tk.Label(root, text="Submit Product Application", font=("TkDefaultFont", 16))
    label.pack()

    product_name_label = tk.Label(root, text="Product Name:")
    product_name_label.pack()

    product_name_entry = tk.Entry(root)
    product_name_entry.pack()

    product_company_label = tk.Label(root, text="Product Company:")
    product_company_label.pack()

    product_company_entry = tk.Entry(root)
    product_company_entry.pack()

    product_category_label = tk.Label(root, text="Product Category:")
    product_category_label.pack()

    product_category_entry = tk.Entry(root)
    product_category_entry.pack()

    product_price_label = tk.Label(root, text="Product Price:")
    product_price_label.pack()

    product_price_entry = tk.Entry(root)
    product_price_entry.pack()

    product_company_website_label = tk.Label(root, text="Company Website:")
    product_company_website_label.pack()

    product_company_website_entry = tk.Entry(root)
    product_company_website_entry.pack()

    product_company_phone_label = tk.Label(root, text="Company Phone Number:")
    product_company_phone_label.pack()

    product_company_phone_entry = tk.Entry(root)
    product_company_phone_entry.pack()

    product_description_label = tk.Label(root, text="Product Description:")
    product_description_label.pack()

    product_description_text = tk.Text(root, height=5, width=30)
    product_description_text.pack()

    # TODO: add checking for phone input
    def on_submit_click():
        product_name = product_name_entry.get()
        product_company = product_company_entry.get()
        product_category = product_category_entry.get()
        product_price = product_price_entry.get()
        product_description = product_description_text.get("1.0", "end")
        product_company_website = product_company_website_entry.get()
        product_company_phone = product_company_phone_entry.get()
        print("Product Name:", product_name)
        print("Product Company:", product_company)
        print("Product Category:", product_category)
        print("Product Price:", product_price)
        print("Product Description:", product_description)
        print("Product Company Website:", product_company_website)
        print("Product Company Phone Number:" , product_company_phone)
        submit_application(product_name, product_company, product_category, product_price, product_description, product_company_phone, product_company_website)

    submit_button = tk.Button(root, text="Submit Application", command=on_submit_click)
    submit_button.pack()

    def on_back_click():
        root.destroy()

    cancel_button = tk.Button(root, text="Cancel", command=on_back_click)
    cancel_button.pack()


def cart_page(cid):
    root = tk.Tk()
    root.title("Products in cart")
    root.geometry("750x500")
    
    pad_label = tk.Label(root, text="       ", font=("TkDefaultFont", 16))
    pad_label.grid(row=0, column=0)
    
    form_label = tk.Label(root, text="Select an order", font=("TkDefaultFont", 16))
    form_label.grid(row=0, column=1)
    
    cursor.execute("""SELECT * FROM [Order]""")
    orders = cursor.fetchall()
    listbox = tk.Listbox(root, width=100, selectmode = 'single')
    for order in orders:
        listbox.insert(tk.END, order)
    listbox.grid(row=1, column=1)
  
    
    def selected_order():
        selection = tuple((listbox.get(listbox.curselection())).strip('()').split(','))
        print(selection[0])
        return(int(selection[0]))
    
    def selected_detail():
        selection = tuple((details_listbox.get(details_listbox.curselection())).strip('()').split(','))
        print(selection)
        return(selection)
 
    def show_details():
        details_listbox.delete(0,tk.END)
        column_info = "Order Num, Product Num, Product Name, Amount, Price"
        details_listbox.insert(tk.END, column_info)
        cursor.execute("{CALL dbo.ReadSpecificOnOrder (?)}", (selected_order()))
        details = cursor.fetchall()
        for detail in details:
            price = str(detail[4])
            detail_string = " {}, {}, {}, {}, ${}".format(detail[0],detail[1],detail[2],detail[3],price)
            details_listbox.insert(tk.END, detail_string)
        

    display_details = tk.Button(root, text='details', command=show_details)
    display_details.grid(row=2, column=1)
    
    details_listbox = tk.Listbox(root, width=100, selectmode = 'single')
    details_listbox.grid(row=3, column=1)
    
   
    def confirm_delete():
        root = tk.Tk()
        root.title("Confirmation Window")
        root.geometry("500x100")
        
        form_label = tk.Label(root, text="Are you sure you want to remove the selected product from your order?", font=("TkDefaultFont", 12))
        form_label.grid(row=0, column=0,columnspan=2)
        
        def delete_from_order():
            cursor.execute("{CALL dbo.DeleteFromOrder (?,?)}", (selected_detail()[0],selected_detail()[1]))
            root.destroy()
            
        def on_back_click():
            root.destroy()
    
        confirm_button = tk.Button(root,text="Yes", command=delete_from_order)
        confirm_button.grid(row=1, column=0)
        
        cancel_button = tk.Button(root, text="Cancel", command=on_back_click)
        cancel_button.grid(row=1, column=1)

    delete_button = tk.Button(root,text="Remove selected product from order", command=confirm_delete)
    delete_button.grid(row=4, column=2)
    
    def on_back_click():
        root.destroy()
    
    cancel_button = tk.Button(root, text="Cancel", command=on_back_click)
    cancel_button.grid(row=4, column=1)   



root = tk.Tk()
root.title("Login")

check_cart = tk.Button(root, text="Cart", command=cart_page)
check_cart.grid(row=4,column=0)

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

register = tk.Button(root, text="Register", command=registration_page)
register.grid(row=5,column=0)

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




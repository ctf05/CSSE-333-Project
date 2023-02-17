import tkinter as tk
from tkinter import ttk

import bcrypt as bcrypt
import pyodbc
import pandas as pd
import openpyxl #this may say it's unused but it's required so make sure you have it
from random import randrange
#My login is ctf05, pass

def connect(server, database, username, password):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return conn


conn = connect("titan.csse.rose-hulman.edu", "OneProductNewTestChristian", "SodaBaseUserbeadlich", "Password123")
conn.autocommit = True
cursor = conn.cursor()
global tree
global combobox
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
global appTable
global ordTable


def click(event):
    maxRange = 10
    try:
        for i in range(0, maxRange):
            y = event.y
            if (y >= (25 + (i * 20)) and y <= (45 + (i * 20))):
                x = event.x
                applicationID = appTable.item(appTable.selection())['values'][0]
                productID = appTable.item(appTable.selection())['values'][1]
                if (x >= 981):
                    cursor.execute("""EXEC dbo.DenyApplication @AppId = ?, @ProdId = ?""", (applicationID, productID))
                elif (x >= 840):
                    cursor.execute("""EXEC dbo.ApproveApplication @AppID = ?, @ProdId = ?""",
                                   (applicationID, productID))
        cursor.execute("""EXEC dbo.getApplicatonInfo""")
        insert_data(cursor.fetchall())
    except IndexError:
        print("Keep your clicks in the box, please")


def clickOrd(event):
    try:
        maxRange = 10
        for i in range(0, maxRange):
            y = event.y
            x = event.x
            if (y >= (25 + (i * 20)) and y <= (45 + (i * 20)) and x >= 700 and x <= 840):
                orderID = ordTable.item(ordTable.selection())['values'][0]
                cursor.execute("""EXEC dbo.ShipOrder @ID = ?""", (orderID))
        cursor.execute("""EXEC dbo.getOrderInfo""")
        insert_data_order(cursor.fetchall())
    except IndexError:
        print("Keep your clicks in the box, please")


def insert_data(data_list):
    global appTable
    for item in appTable.get_children():
        appTable.delete(item)
    i = 0
    for row in data_list:
        # if (row[5] != "Pending"):
        #     continue
        appTable.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5], "~ Approve ~", "~ Deny ~"))
        i += 1


def insert_data_order(data_list):
    global ordTable
    for item in ordTable.get_children():
        ordTable.delete(item)
    i = 0
    for row in data_list:
        ordTable.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], "~ Ship ~"))
        i += 1

def insertDataIntoSQL(): #Assumes you are submitting a minimum of 12 products and 5 users.
    #product, application, customer, supplier, category, billing info, login,
    storedProcedureArray = ["{CALL SubmitProductApplication (?, ?, ?, ?, ?, ?, ?)}", "{CALL RegisterUser (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)}", "The orders insertion is randomized and doesn't use an excel file"]
    checkArray = ["{CALL ReadProduct}", "{CALL ReadCustomer}", "{CALL ReadOrder}"]
    # Load the Excel data into a Pandas dataframe
    excelFileArray = ["ProductApplication.xlsx", "Customer.xlsx"]

    # Loop through each row in the dataframe
    for i in range(0, len(storedProcedureArray)):
        if i != 2:
            df = pd.read_excel(excelFileArray[i])
        result1 = cursor.execute(checkArray[i])
        results1Len = len(result1.fetchall())
        for index, row in df.iterrows():
            row = row.astype(str).tolist()
            if i == 2:
                for z in range(0, 10):
                    cursor.execute(
                        """SET NOCOUNT ON;DECLARE @orderID int;EXEC [dbo].[addOrder] @CustomerID = ?, @OrderID = @orderID OUTPUT;SELECT @orderID AS the_output;""",
                        (randrange(1, 5)))
                    order_id = (cursor.fetchone())[0]
                    maxRange = randrange(1, 3)
                    for i in range(0, maxRange):
                        cursor.execute("{CALL dbo.addToOrder (?,?,?)}", (order_id, randrange(0, 9), randrange(1, 5)))
            else:
                # Call the stored procedure to insert the row into the database
                cursor.execute(storedProcedureArray[i], row)
                if i == 0:
                    cursor.execute("EXEC dbo.UpdateProduct @ID = ?, @NumberInStock = ?", (index + 1, randrange(1000, 2000)))
                    if index < 10:
                        cursor.execute("{CALL ApproveApplication (?,?)}", (index + 1, index + 1))
        result2 = cursor.execute(checkArray[i])
        results2Len = len(result2.fetchall())
        # Check for errors
        if results1Len == results2Len:
            print(results1Len)
            print(results2Len)
            status_page("Data Insert", f"Error inserting row: {index} Excel File: {excelFileArray[i]} Stored Procedure: {storedProcedureArray[i]}")
            break
        else:
            status_page("Data Insert", "Success")
    # cursor.execute("""EXEC dbo.getApplicatonInfo""")
    # insert_data(cursor.fetchall())
    # cursor.execute("""EXEC dbo.getOrderInfo""")
    # insert_data_order(cursor.fetchall())



def login_success():
    root = tk.Tk()
    root.geometry("1250x500")
    root.title("Admin Control Panel")

    # Create a dropdown menu
    global combobox
    combobox_label = ttk.Label(root, text="Applications:")
    global appTable
    global ordTable
    # Create a table to display data
    appTable = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"),
                            show='headings')
    appTable.heading("col1", text="Application ID")
    appTable.column("col1", width=140, anchor="center")
    appTable.heading("col2", text="Product ID")
    appTable.column("col2", width=140, anchor="center")
    appTable.heading("col3", text="Product Name")
    appTable.column("col3", width=140, anchor="center")
    appTable.heading("col4", text="Category Name")
    appTable.column("col4", width=140, anchor="center")
    appTable.heading("col5", text="Date")
    appTable.column("col5", width=140, anchor="center")
    appTable.heading("col6", text="Status")
    appTable.column("col6", width=140, anchor="center")
    appTable.heading("col7", text="Approve Button")
    appTable.column("col7", width=140, anchor="center")
    appTable.heading("col8", text="Deny Button")
    appTable.column("col8", width=140, anchor="center")
    appTable.grid(row=10, column=0, columnspan=4, padx=5, pady=10)
    cursor.execute("""EXEC dbo.getApplicatonInfo""")
    insert_data(cursor.fetchall())
    appTable.bind("<Double-1>", click)

    ordTable = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5", "col7"), show='headings')
    ordTable.heading("col1", text="Order ID")
    ordTable.column("col1", width=140, anchor="center")
    ordTable.heading("col2", text="Customer ID")
    ordTable.column("col2", width=140, anchor="center")
    ordTable.heading("col3", text="Date Name")
    ordTable.column("col3", width=140, anchor="center")
    ordTable.heading("col4", text="Address")
    ordTable.column("col4", width=140, anchor="center")
    ordTable.heading("col5", text="ShipDate")
    ordTable.column("col5", width=140, anchor="center")
    ordTable.heading("col7", text="Ship Button")
    ordTable.column("col7", width=140, anchor="center")
    ordTable.grid(row=12, column=2, columnspan=4, padx=5, pady=10)
    cursor.execute("""EXEC dbo.getOrderInfo""")
    insert_data_order(cursor.fetchall())
    ordTable.bind("<Double-1>", clickOrd)

    product_button = tk.Button(root, text="Update Products", command=view_admin_product)
    product_button.grid(row=12, column=0)
    Data_button = tk.Button(root, text="Import Data", command=insertDataIntoSQL)
    Data_button.grid(row=12, column=1)


def view_admin_product():
    root = tk.Tk()
    root.geometry("1250x500")
    root.title("Admin Control Panel")

    label = ttk.Label(root, text="Admin Products Page", font=("TkDefaultFont", 14, "bold"))
    label.pack(pady=10)

    pTable = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"), show="headings")
    pTable.heading("col1", text="Product ID")
    pTable.column("col1", width=140, anchor="center")
    pTable.heading("col2", text="Name")
    pTable.column("col2", width=140, anchor="center")
    pTable.heading("col3", text="Supplier")
    pTable.column("col3", width=140, anchor="center")
    pTable.heading("col4", text="Category")
    pTable.column("col4", width=140, anchor="center")
    pTable.heading("col5", text="Price")
    pTable.column("col5", width=140, anchor="center")
    pTable.heading("col6", text="Stock Level")
    pTable.column("col6", width=140, anchor="center")
    pTable.heading("col7", text="For Sale")
    pTable.column("col7", width=140, anchor="center")
    pTable.pack(pady=10)

    def insert_data_home(data_list):
        for item in pTable.get_children():
            pTable.delete(item)
        for row in data_list:
            pTable.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    def get_products():
        cursor.execute("""Exec dbo.AdminViewProducts""")

        data_list = cursor.fetchall()
        pids = []
        insert_data_home(data_list)

    get_products()

    frame = ttk.Frame(root)
    frame.pack(pady=10)

    price_label = ttk.Label(frame, text="Product Price:")
    price_label.pack(side="left", padx=10)

    price_entry = ttk.Entry(frame)
    price_entry.pack(side="left", padx=10)

    stock_label = ttk.Label(frame, text="Stock Level:")
    stock_label.pack(side="left", padx=10)

    stock_entry = ttk.Entry(frame)
    stock_entry.pack(side="left", padx=10)

    for_sale_label = ttk.Label(frame, text="For Sale:")
    for_sale_label.pack(side="left", padx=10)

    for_sale_entry = ttk.Entry(frame)
    for_sale_entry.pack(side="left", padx=10)

    def update_products():
        sTitle = "Product Update"
        price = price_entry.get()
        stock = stock_entry.get()
        forSale = for_sale_entry.get()

        if forSale == "":
            forSale = None

        if price == "":
            price = None

        if stock == "":
            stock = None

        if price == None or price.isnumeric():
            print("price is good")
        else:
            try:
                float(price)
            except:
                status_page(sTitle, "Price is not a number")
                return

        if stock == None or stock.isdigit():
            print("stock is good")
        else:
            status_page(sTitle, "Stock is not a number")
            return

        if forSale == None:
            print("For Sale good")
        elif forSale.lower() == "true" or forSale == "1":
            forSale = 1
        elif forSale.lower() == "false" or forSale == "0":
            forSale = 0
        else:
            status_page(sTitle, "Please make a valid input for 'For Sale'.\n Valid inputs are: True or False")
            return

        sel = pTable.selection()
        if len(sel) == 0:
            status_page(sTitle, "Please make a selection before submitting")
            return

        # item = pTable.item(sel[0])
        # pid = item.get('values')[0]

        try:
            for k in range(len(sel)):
                item = pTable.item(sel[k])
                pid = item.get('values')[0]
                cursor.execute("""EXEC dbo.UpdateProduct @ID = ?, @Price = ?, @NumberInStock = ?, @ForSale = ?""",
                               (pid, price, stock, forSale))

            get_products()

            if stock != None or price != None or forSale != None:
                for_sale_entry.delete(0, tk.END)
                price_entry.delete(0, tk.END)
                stock_entry.delete(0, tk.END)
                status_page(sTitle, "Update Success")
        except:
            status_page(sTitle, "Error updating products")

    submit_button = ttk.Button(root, text="Submit", command=update_products)
    submit_button.pack(pady=10)

    close_button = ttk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=10)

def status_page(title, message):
    confirm_root = tk.Tk()
    confirm_root.title(title)
    confirm_root.geometry("250x200")

    confirm = tk.Label(confirm_root, text=message, font=("TkDefaultFont", 16))
    confirm.grid(row=0, column=0)

    def on_back_click():
        confirm_root.destroy()

    ok_button = tk.Button(confirm_root, text="Ok", command=on_back_click)
    ok_button.grid()


def login_failure():
    status_page("Login", "Username or Password Incorrect")


def check_credentials():
    # check if the entered username and password match
    # the expected values
    global password_entry

    if username_entry.get() == "admin" and password_entry.get() == "password":
        login_success()
        return

    if username_entry.get() == "a" and password_entry.get() == "123":
        login_success()
        return

    password = password_entry.get().encode()

    cursor.execute("""Exec dbo.PasswordSaltFromUsername @uname = ?""", (username_entry.get()))
    try:
        password_salt = cursor.fetchone()[0].encode()
        password_hash = bcrypt.hashpw(password, password_salt)

        cursor.execute("""Exec dbo.CheckPasswordHash @hash = ?""", (password_hash.decode()[0:49]))
        try:
            print(password_hash.decode()[0:49])
            user = cursor.fetchone()
            print(user)
            print(user[1])
            home_page(user[1])
        except:
            print("Password incorrect")
            login_failure()
    except:
        print("Username not found")
        login_failure()


def home_page(cid):
    root = tk.Tk()
    root.geometry("1250x500")
    root.title("Home Page")

    global order
    order = []

    global pids
    pids = []

    def view_cart_page():
        cart_page(cid, order)

    def view_order_page():
        order_page(cid)

    # Create a dropdown menu
    label = ttk.Label(root, text="Welcome to One Product", font=("TkDefaultFont", 14, "bold"))
    label.pack(pady=10)

    cursor.execute("""Exec dbo.AllCategories""")
    cats = cursor.fetchall()
    options = ["All", "All"]
    for row in cats:
        options.append(row[0])

    var = tk.StringVar(root)
    var.set(options[0])

    def update_option(event):
        var.set(event)
        print(var.get())
        if var.get() == "All":
            get_products(None)
        else:
            get_products(var.get())

    frame = ttk.Frame(root)
    frame.pack(pady=10)

    dropdown = ttk.OptionMenu(frame, var, *options, command=update_option)
    dropdown.pack(side="left")

    order_button = ttk.Button(frame, text="View Orders", command=view_order_page)
    order_button.pack(side="left", padx=10)

    cart_button = ttk.Button(frame, text="View Cart", command=view_cart_page)
    cart_button.pack(side="left")

    # Create a table to display data
    pTable = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4"), show='headings')
    # pTable.heading("col1", text="Product ID")
    # pTable.column("col1", width=140, anchor="center")
    pTable.heading("col1", text="Name")
    pTable.column("col1", width=140, anchor="center")
    pTable.heading("col2", text="Category")
    pTable.column("col2", width=140, anchor="center")
    pTable.heading("col3", text="Price")
    pTable.column("col3", width=140, anchor="center")
    pTable.heading("col4", text="Quantity")
    pTable.column("col4", width=140, anchor="center")
    pTable.pack(pady=10)

    # pTable.grid(row=10, column=0, columnspan=4, padx=5, pady=10)
    # cursor.execute("""EXEC dbo.AllProductsForSale""")

    def insert_data_home(data_list):
        for item in pTable.get_children():
            pTable.delete(item)
        for row in data_list:
            pTable.insert("", tk.END, values=(row[1], row[2], row[3], row[4]))
            pids.append(row[0])

    # data_list = cursor.fetchall()
    # pids = []
    # insert_data_home(data_list)

    def get_products(catName):
        if catName == None:
            cursor.execute("""Exec dbo.AllProductsForSale""")
        else:
            cursor.execute("""Exec dbo.ProductsWithCategory @cat = ?""", catName)

        data_list = cursor.fetchall()
        pids = []
        insert_data_home(data_list)

    get_products(None)

    def go_to_product(event):
        selected_item = pTable.selection()
        # test = pTable.item(selected_item[0])
        index = pTable.index(selected_item[0])
        pid = pids[index]
        open_product_page(pid, order)
        # csIndex = listbox.curselection()[0]
        # pid = listbox.get(csIndex).split(",")[0][1:]
        # open_product_page(pid, order)

    pTable.bind("<Double-1>", go_to_product)

    close_button = ttk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=10)


def open_product_page(productID, order):
    root = tk.Tk()
    root.title("Product Details")
    root.geometry("800x600")

    cursor.execute("""Exec dbo.ProductFromID @pid = ?""", productID)
    data_list = cursor.fetchone()
    print(data_list)

    label = ttk.Label(root, text=data_list[0], font=("Arial", 18, "bold"))
    label.pack(pady=10)

    # create frame to hold widgets
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # create labels and text boxes for product details
    company_label = tk.Label(frame, text="Company:", font=("Arial", 13))
    company_label.grid(row=0, column=0, padx=5, pady=5)
    company_text = tk.Text(frame, height=1, width=20, font=("Arial", 13))
    company_text.grid(row=0, column=1, padx=5, pady=5)

    category_label = tk.Label(frame, text="Category:", font=("Arial", 13))
    category_label.grid(row=1, column=0, padx=5, pady=5)
    category_text = tk.Text(frame, height=1, width=20, font=("Arial", 13))
    category_text.grid(row=1, column=1, padx=5, pady=5)

    price_label = tk.Label(frame, text="Price:", font=("Arial", 13))
    price_label.grid(row=2, column=0, padx=5, pady=5)
    price_text = tk.Text(frame, height=1, width=20, font=("Arial", 13))
    price_text.grid(row=2, column=1, padx=5, pady=5)

    quantity_label = tk.Label(frame, text="Quantity:", font=("Arial", 13))
    quantity_label.grid(row=3, column=0, padx=5, pady=5)
    quantity_text = tk.Text(frame, height=1, width=20, font=("Arial", 13))
    quantity_text.grid(row=3, column=1, padx=5, pady=5)

    description_label = tk.Label(frame, text="Description:", font=("Arial", 13))
    description_label.grid(row=4, column=0, padx=5, pady=5)
    description_text = tk.Text(frame, height=6, width=20, font=("Arial", 13))
    description_text.grid(row=4, column=1, padx=5, pady=5)

    # populate the text boxes with some sample data
    company_text.insert("end", data_list[1])
    category_text.insert("end", data_list[2])
    price_text.insert("end", data_list[3])
    quantity_text.insert("end", data_list[4])
    description_text.insert("end", data_list[5])

    company_text.config(state="disabled")
    category_text.config(state="disabled")
    price_text.config(state="disabled")
    quantity_text.config(state="disabled")
    description_text.config(state="disabled")

    def add_to_order():
        root = tk.Tk()
        root.title("Confirmation Window")
        root.geometry("500x100")
        
        form_label = tk.Label(root, text="How many would you like to purchase", font=("TkDefaultFont", 12))
        form_label.pack()
        
        amount_entry = tk.Entry(root)
        amount_entry.pack()
        
        def display_error(stock):
            error_root = tk.Tk()
            error_root.title("ERROR")
            error_root.geometry("250x200")
            
            error_message = "Not enough product in stock. ? remain in stock.".format(stock)
            error = tk.Label(error_root, text="Not enough product in stock", font=("TkDefaultFont", 16))
            error.pack()
            
            def on_back_click():
                root.destroy()
            
            cancel_button = tk.Button(root, text="Close", command=on_back_click)
            cancel_button.pack()

        def add():
            amount = amount_entry.get()

            if not amount.isnumeric():
                status_page("Order Error", "Please enter a number")
            
            cursor.execute("{CALL dbo.ReadProductSpecific (?)}",(productID))
            stock = (cursor.fetchone())[2]
            
            if(int(amount)>int(stock)):
                display_error(stock)
            else:
                print(amount)
                order.append([productID,amount])
                root.destroy()
                status_page("Order", "Added To Cart")
            
        def on_back_click():
            root.destroy()
    
        confirm_button = tk.Button(root,text="Confirm", command=add)
        confirm_button.pack()
        
        cancel_button = tk.Button(root, text="Cancel", command=on_back_click)
        cancel_button.pack()


    add_button = tk.Button(root, text="Add To Order", command=add_to_order)
    add_button.pack()

    # add close button at the bottom
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(side="bottom", pady=10)



def submit_application(name, company, category, price, description, phone, website):
    title = "Application"

    if name == "" or company == "" or category == "" or price == "" or description == "" or phone == "" or website == "":
        status_page(title, "Please fill out all input fields")
        return False

    if price.isnumeric():
        print("price is good")
    else:
        try:
            float(price)
        except:
            status_page(title, "Price Input is not a number")
            return False

    if not check_phone_input(phone):
        status_page(title, "Incorrect Phone Input, please input as: xxx-xxx-xxxx")
        return False

    try:
        cursor.execute(
            """EXEC dbo.SubmitProductApplication @PName = ?, @CatName = ?, @SName = ?, @PDesc = ?, @ProPrice = ?, @SPhone = ?, @SWebsite = ?""",
            (name, category, company, description, price, phone, website))

        status_page(title, "Application Successfully Submited")
        return True
    except:
        status_page(title, "Error Submitting Application")
        return False


def check_phone_input(phone):
    if len(phone) != 12:
        print("len fault")
        return False

    for k in range(12):
        if k == 3 or k == 7:
            if not phone[k] == "-":
                print("- fault")
                return False
        else:
            if not phone[k].isdigit():
                print("digit fault")
                return False

    return True


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
    password_entry = tk.Entry(root, show="*")
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
    submitRegister.grid(row=10, column=0)


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

    title = "Register User"

    if username == "" or password == "" or first_name == "" or last_name == "" or address == "" or phone == "" or card == "" or expiration == "" or security == "" or card_type == "":
        status_page(title, "Please fill out all inputs")
        return

    if not check_phone_input(phone):
        status_page(title, "Please enter vaild input for phone number: input as xxx-xxx-xxxx")
        return

    if len(card) != 16 or not card.isnumeric():
        status_page(title, "Invalid input for Card Number")
        return

    if len(security) != 3 or not security.isnumeric():
        status_page(title, "Security Code is not a 3 digit number")
        return

    if not check_date(expiration):
        status_page(title, "Please format exirpation date as: year-month-day, xxxx-xx-xx")
        return

    if card_type != "Credit" and cart_page != "Debit":
        status_page(title, "Invalid Card Type")
        return

    try:
        cursor.execute("EXEC dbo.RegisterUser @UserName = ?, @PasswordSalt = ?, @PasswordHash = ?, @Address = ?, "
                       "@FName = ?, @LName = ?, @Phone = ?, @CardType = ?, @CardNumber = ?, @ExperationDate = ?, @SecurityCode = ?",
                       (username, password_salt.decode(), password_hash.decode()[0:49], address, first_name, last_name,
                        phone, card_type,
                        card, expiration, security))
        status_page(title, "Registration Success")
        username = username_entry.delete(0, tk.END)
        password = password_entry.delete(0, tk.END)
        first_name = first_name_entry.delete(0, tk.END)
        last_name = last_name_entry.delete(0, tk.END)
        address = address_entry.delete(0, tk.END)
        phone = phone_entry.delete(0, tk.END)
        card = card_entry.delete(0, tk.END)
        expiration = expiration_entry.delete(0, tk.END)
        security = security_entry.delete(0, tk.END)
        card_type = card_type_entry.delete(0, tk.END)
    except:
        status_page(title, "Error Registering User")


def check_date(date):
    if len(date) != 10:
        return False

    for k in range(10):
        if k == 4 or k == 7:
            if not date[k] == "-":
                return False
        else:
            if not date[k].isdigit():
                return False

    return True


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

    # TODO: add checking for phone input and others
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
        print("Product Company Phone Number:", product_company_phone)

        status = submit_application(product_name, product_company, product_category, product_price, product_description,
                                    product_company_phone, product_company_website)

        if status:
            product_name = product_name_entry.delete(0, tk.END)
            product_company = product_company_entry.delete(0, tk.END)
            product_category = product_category_entry.delete(0, tk.END)
            product_price = product_price_entry.delete(0, tk.END)
            product_description = product_description_text.delete(1.0, tk.END)
            product_company_website = product_company_website_entry.delete(0, tk.END)
            product_company_phone = product_company_phone_entry.delete(0, tk.END)

    submit_button = tk.Button(root, text="Submit Application", command=on_submit_click)
    submit_button.pack()

    def on_back_click():
        root.destroy()

    cancel_button = tk.Button(root, text="Cancel", command=on_back_click)
    cancel_button.pack()


def cart_page(cid, order):
    root = tk.Tk()
    root.title("Cart")
    root.geometry("750x500")

    pad_label = tk.Label(root, text="       ", font=("TkDefaultFont", 16))
    pad_label.grid(row=0, column=0)

    form_label = tk.Label(root, text="Review order", font=("TkDefaultFont", 16))
    form_label.grid(row=0, column=1)

    order_label = tk.Label(root, text="Product, Amount, Price", font=("TkDefaultFont", 10))
    order_label.grid(row=1, column=1, sticky='W')

    item_listbox = tk.Listbox(root, width=100, selectmode='single')

    for item in order:
        cursor.execute("{CALL dbo.ReadProductSpecific (?)}", (item[0]))
        product = cursor.fetchone()
        prod_name = product[0]
        price = int(item[1]) * int(product[1])

        item_string = "    {},    {},    {}".format(prod_name, item[1], price)
        item_listbox.insert(tk.END, item_string)
    item_listbox.grid(row=2, column=1)


    # address_entry = tk.Entry(root)
    # address_entry.grid(row=3, column=1)

    def confirm_order():
        confirm_root = tk.Tk()
        confirm_root.title("Success")
        confirm_root.geometry("250x200")

        confirm = tk.Label(confirm_root, text="Order Placed", font=("TkDefaultFont", 16))
        confirm.grid(row=0, column=0)

        def on_back_click():
            confirm_root.destroy()

        ok_button = tk.Button(confirm_root, text="Ok", command=on_back_click)
        ok_button.grid(row=2, column=0)

    def submit_order():
        # address = address_entry.get()

        if len(order) == 0:
            status_page("Cart Page", "Nothing In Cart")
            return

        cursor.execute(
            """SET NOCOUNT ON;DECLARE @orderID int;EXEC [dbo].[addOrder] @CustomerID = ?, @OrderID = @orderID OUTPUT;SELECT @orderID AS the_output;""",
            (cid))
        order_id = (cursor.fetchone())[0]
        print(order_id)
        for item in order:
            cursor.execute("{CALL dbo.addToOrder (?,?,?)}", (order_id, item[0], item[1]))

        order.clear()
        root.destroy()
        confirm_order()

    def on_back_click():
        root.destroy()

    submit_button = tk.Button(root, text="Place order", command=submit_order)
    submit_button.grid(row=4, column=1)

    cancel_button = tk.Button(root, text="Cancel", command=on_back_click)
    cancel_button.grid(row=6, column=1)


def order_page(cid):
    root = tk.Tk()
    root.title("Current Orders")
    root.geometry("750x500")

    pad_label = tk.Label(root, text="       ", font=("TkDefaultFont", 16))
    pad_label.grid(row=0, column=0)

    form_label = tk.Label(root, text="Select an order", font=("TkDefaultFont", 16))
    form_label.grid(row=0, column=1)

    order_label = tk.Label(root, text="Order Number, Order Date, Address, Shipping Date", font=("TkDefaultFont", 10))
    order_label.grid(row=1, column=1, sticky='W')

    cursor.execute("{CALL dbo.ReadCustomerOrders (?)}", (cid))
    orders = cursor.fetchall()
    listbox = tk.Listbox(root, width=100, selectmode='single')
    for order in orders:
        date = str(order[1])
        ship_date = str(order[3])
        order_string = "    {},    {},    {},    {}".format(order[0], date, order[2], ship_date)
        listbox.insert(tk.END, order_string)
    listbox.grid(row=2, column=1)

    def selected_order():
        selection = tuple((listbox.get(listbox.curselection())).strip('()').split(','))
        print(selection[0])
        return (int(selection[0]))

    def selected_detail():
        selection = tuple((details_listbox.get(details_listbox.curselection())).strip('()').split(','))
        print(selection)
        return (selection)

    def show_details():
        details_listbox.delete(0, tk.END)
        cursor.execute("{CALL dbo.ReadSpecificOnOrder (?)}", (selected_order()))
        details = cursor.fetchall()
        for detail in details:
            price = str(detail[4])
            detail_string = "    {},    {},    {},    {},    ${}".format(detail[0], detail[1], detail[2], detail[3],
                                                                         price)
            details_listbox.insert(tk.END, detail_string)

    display_details = tk.Button(root, text='details', command=show_details)
    display_details.grid(row=3, column=1)

    detail_label = tk.Label(root, text="Order Number, Product Number, Product Name, Amount, Price",
                            font=("TkDefaultFont", 10))
    detail_label.grid(row=4, column=1, sticky='W')

    details_listbox = tk.Listbox(root, width=100, selectmode='single')
    details_listbox.grid(row=5, column=1)

    def confirm_delete():
        root = tk.Tk()
        root.title("Confirmation Window")
        root.geometry("500x100")

        form_label = tk.Label(root, text="Are you sure you want to remove the selected product from your order?",
                              font=("TkDefaultFont", 12))
        form_label.grid(row=0, column=0, columnspan=2)

        def delete_from_order():
            cursor.execute("{CALL dbo.DeleteFromOrder (?,?)}", (selected_detail()[0], selected_detail()[1]))
            root.destroy()

        def on_back_click():
            root.destroy()

        confirm_button = tk.Button(root, text="Yes", command=delete_from_order)
        confirm_button.grid(row=1, column=0)

        cancel_button = tk.Button(root, text="Cancel", command=on_back_click)
        cancel_button.grid(row=1, column=1)

    # delete_button = tk.Button(root, text="Remove selected product from order", command=confirm_delete)
    # delete_button.grid(row=4, column=2)

    def on_back_click():
        root.destroy()

    cancel_button = tk.Button(root, text="Cancel", command=on_back_click)
    cancel_button.grid(row=6, column=1)


root = tk.Tk()
root.title("Login")
root.geometry("500x400")

username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=4)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=4)

username_entry = tk.Entry(root)
username_entry.grid(row=0, column=5, columnspan=10)

password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=5, columnspan=10)

login_picture = tk.PhotoImage(file='login.png').subsample(5)
login_button = tk.Button(root, image=login_picture, command=check_credentials)
login_button.grid(row=5, column=1, columnspan=5)

app_picture = tk.PhotoImage(file='SubmitProduct.png').subsample(5)
add_product_button = tk.Button(root, image=app_picture, command=application_page)
add_product_button.grid(row=5, column=10, columnspan=5)

register_picture = tk.PhotoImage(file='register.png').subsample(5)
register = tk.Button(root, image=register_picture, command=registration_page)
register.grid(row=5, column=15, columnspan=5)

Data_button = tk.Button(root, text="Import Data", command=insertDataIntoSQL)
Data_button.grid(row=12, column=1)

root.mainloop()


def execute_stored_procedure(conn):
    # connect to the SQL Server instance

    # call the stored procedure and pass the values of the dropdown menus as parameters
    ##cursor.execute("{CALL dbo.addCustomer (?,?,?,?,?)}", ("fname", "lname", "123-545-3443", "jonesville", None))
    cursor.execute("{CALL dbo.addCustomer ('re','ree','123-454-3232','jone',null)}")
    # retrieve the results of the stored procedure
    # results = cursor.fetchall()
    # close the connection to the SQL Server instance
    cursor.close()
    conn.close()
    # return results

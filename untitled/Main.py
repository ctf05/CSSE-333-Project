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
    maxRange = len(appTable.item(appTable.selection())['values'])
    for i in range(0, maxRange):
        y = event.y
        if (y >= (25 + (i * 20)) and y <= (45 + (i * 20))):
            x = event.x
            applicationID = appTable.item(appTable.selection())['values'][0]
            productID = appTable.item(appTable.selection())['values'][1]
            if (x >= 981):
                cursor.execute("""EXEC dbo.DenyApplication @AppId = ?, @ProdId = ?""", (applicationID, productID))
            elif (x >= 840):
                cursor.execute("""EXEC dbo.ApproveApplication @AppID = ?, @ProdId = ?""", (applicationID, productID))
    cursor.execute("""EXEC dbo.getApplicatonInfo""")
    insert_data(cursor.fetchall())

def clickOrd(event):
    maxRange = len(ordTable.item(ordTable.selection())['values'])
    for i in range(0, maxRange):
        y = event.y
        x = event.x
        if (y >= (25 + (i * 20)) and y <= (45 + (i * 20)) and x >= 700 and x <= 840):
            orderID = ordTable.item(ordTable.selection())['values'][0]
            cursor.execute("""EXEC dbo.ShipOrder @ID = ?""", (orderID))
    cursor.execute("""EXEC dbo.getOrderInfo""")
    insert_data_order(cursor.fetchall())


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
    appTable = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"), show='headings')
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
    appTable.heading("col6", text="ShippedData")
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
    ordTable.grid(row=12, column=1, columnspan=4, padx=5, pady=10)
    cursor.execute("""EXEC dbo.getOrderInfo""")
    insert_data_order(cursor.fetchall())
    ordTable.bind("<Double-1>", clickOrd)

    product_button = tk.Button(root, text="Update Products", command=view_admin_product)
    product_button.grid(row=12, column=0)

def view_admin_product():
    root = tk.Tk()
    root.geometry("1250x500")
    root.title("Admin Control Panel")

    label = tk.Label(root, text="Admin Products Page", font=("TkDefaultFont", 16))
    label.pack()

    listbox = tk.Listbox(root, width=100)
    listbox.pack()

    product_price_label = tk.Label(root, text="Product Price:")
    product_price_label.pack()

    product_price_entry = tk.Entry(root)
    product_price_entry.pack()

    product_stock_label = tk.Label(root, text="Number In Stock:")
    product_stock_label.pack()

    product_stock_entry = tk.Entry(root)
    product_stock_entry.pack()

    product_forSale_label = tk.Label(root, text="For Sale:")
    product_forSale_label.pack()

    product_forSale_entry = tk.Entry(root)
    product_forSale_entry.pack()

    def get_products():
        cursor.execute("""Select * From Product""")
        
        products = cursor.fetchall()
        listbox.delete(0, tk.END)
        
        for product in products:
            listbox.insert(tk.END, product)
        listbox.pack()

    def update_success_page():       

        confirm_root = tk.Tk()
        confirm_root.title("Success")
        confirm_root.geometry("250x200")
            
        confirm = tk.Label(confirm_root, text="Update Success", font=("TkDefaultFont", 16))
        confirm.grid(row=0,column=0)
            
        def on_back_click():
            confirm_root.destroy()
            
        ok_button = tk.Button(confirm_root, text="Ok", command=on_back_click)
        ok_button.grid()

    def update_products():
        price = product_price_entry.get()
        stock = product_stock_entry.get()
        forSale = product_forSale_entry.get()

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
                float(stock)
            except:
                print("price bad")
                return

        if stock == None or stock.isdigit():
            print("stock is good")
        else:
             print("stock bad")
             return
        
        if forSale == None:
            print("For Sale good")
        elif forSale.lower() == "true":
            forSale = 1
        elif forSale.lower() == "false":
            forSale = 0
        else:
            print("For sale bad")
            return

        if len(listbox.curselection()) == 0:
            print("no selection")
            return

        csIndex = listbox.curselection()[0]
        productInfo = listbox.get(csIndex).split(",")
        pid = productInfo[0][1:]
        
        cursor.execute("""EXEC dbo.UpdateProduct @ID = ?, @Price = ?, @NumberInStock = ?, @ForSale = ?""", (pid, price, stock, forSale))
        get_products()

        if stock != None or price != None or forSale != None:
            product_forSale_entry.delete(0, tk.END)
            product_price_entry.delete(0, tk.END)
            product_stock_entry.delete(0, tk.END)
            update_success_page()
        

    submit_button = tk.Button(root, text="Submit", command=update_products)
    submit_button.pack()

    get_products()

    


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

    if username_entry.get() == "a" and password_entry.get() == "123":
        login_success()
        return

    password = password_entry.get().encode()

    cursor.execute("""
        SELECT PasswordSalt
        FROM Login
        WHERE Username = ?""",(username_entry.get()))
    try:
        password_salt = cursor.fetchone()[0].encode()
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
    except:
        print("Username not found")
        login_failure()


def home_page(cid):
    root = tk.Tk()
    root.title("Home Page")
    root.geometry("1250x500")
    
    global order 
    order = []

    global products
    products = []

    def go_to_product(event):
        print("go to product")
        csIndex = listbox.curselection()[0]
        pid = listbox.get(csIndex).split(",")[0][1:]
        open_product_page(pid,order)

    label = tk.Label(root, text="Welcome to One Product", font=("TkDefaultFont", 16))
    label.pack()
    
    listbox = tk.Listbox(root, width=100)
    listbox.pack()   


    def show_choice(event):
        print("show choice")
        print(var.get())
        if var.get() == "All":
            get_products(None)
        else:
            get_products(var.get())

    def get_products(catName):
        if catName == None:
            cursor.execute("""Select * From Product Where ForSale = 1""")
        else:
            cursor.execute("""Select * From Product P Join Category C On P.CategoryID = C.CategoryID Where ForSale = 1 And C.Name = ?""", catName)
        
        products = cursor.fetchall()
        listbox.delete(0, tk.END)
        
        for product in products:
            listbox.insert(tk.END, product)
        listbox.bind("<Double-1>", go_to_product)
        listbox.pack()

    get_products(None)

    cursor.execute("""Select Name From Category""")
    cats = cursor.fetchall()
    options = ["All"]
    for row in cats:
        options.append(row[0])

    var = tk.StringVar()
    var.set(options[0]) # default value

    dropdown = tk.OptionMenu(root, var, *options, command=show_choice)
    dropdown.pack()

    def view_cart_page():
        cart_page(cid,order)
        
    def view_order_page():
        order_page(cid)


    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack()

    cart_button = tk.Button(root, text="View Cart", command=view_cart_page)
    cart_button.pack()
    
    order_button = tk.Button(root, text="View Orders", command=view_order_page)
    order_button.pack()

def open_product_page(productID,order):
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
            
            cursor.execute("{CALL dbo.ReadProductSpecific (?)}",(productID))
            stock = (cursor.fetchone())[2]
            
            if(int(amount)>int(stock)):
                display_error(stock)
            else:
                print(amount)
                order.append([productID,amount])
                root.destroy()
            
        def on_back_click():
            root.destroy()
    
        confirm_button = tk.Button(root,text="Confirm", command=add)
        confirm_button.pack()
        
        cancel_button = tk.Button(root, text="Cancel", command=on_back_click)
        cancel_button.pack()
              
    def on_back_click():
        product_page.destroy()


    add_button = tk.Button(product_page,text="Add To Order", command=add_to_order)
    add_button.pack()  
    
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
        print("Product Company Phone Number:" , product_company_phone)

        if not check_phone_input():
            return

        submit_application(product_name, product_company, product_category, product_price, product_description, product_company_phone, product_company_website)

    submit_button = tk.Button(root, text="Submit Application", command=on_submit_click)
    submit_button.pack()

    def on_back_click():
        root.destroy()

    cancel_button = tk.Button(root, text="Cancel", command=on_back_click)
    cancel_button.pack()

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


def cart_page(cid,order):
    root = tk.Tk()
    root.title("Cart")
    root.geometry("750x500")
    
    pad_label = tk.Label(root, text="       ", font=("TkDefaultFont", 16))
    pad_label.grid(row=0, column=0)
    
    form_label = tk.Label(root, text="Review order", font=("TkDefaultFont", 16))
    form_label.grid(row=0, column=1)
    
    order_label = tk.Label(root, text="Product, Amount, Price", font=("TkDefaultFont", 10))
    order_label.grid(row=1, column=1,sticky='W')
    
    item_listbox = tk.Listbox(root, width=100, selectmode = 'single')
    
    for item in order:
        
        cursor.execute("{CALL dbo.ReadProductSpecific (?)}",(item[0]))
        product = cursor.fetchone()
        prod_name = product[0]
        price = int(item[1])*int(product[1])
        
        item_string = "    {},    {},    {}".format(prod_name,item[1],price)
        item_listbox.insert(tk.END, item_string)
    item_listbox.grid(row=2, column=1)
    
    
    address_entry = tk.Entry(root)
    address_entry.grid(row=3, column=1)
    
    def confirm_order():
        confirm_root = tk.Tk()
        confirm_root.title("Success")
        confirm_root.geometry("250x200")
            
        confirm = tk.Label(confirm_root, text="Order Placed", font=("TkDefaultFont", 16))
        confirm.grid(row=0,column=0)
            
        def on_back_click():
            confirm_root.destroy()
            
        ok_button = tk.Button(root, text="Ok", command=on_back_click)
        ok_button.grid(row=2,column=0)
    
    def submit_order():
        address = address_entry.get()
        
        cursor.execute("""SET NOCOUNT ON;DECLARE @orderID int;EXEC [dbo].[addOrder] @CustomerID = ?, @ShipAddress = ?,@OrderID = @orderID OUTPUT;SELECT @orderID AS the_output;""",(cid,address))
        order_id = (cursor.fetchone())[0]
        print(order_id)
        for item in order:
            cursor.execute("{CALL dbo.addToOrder (?,?,?)}",(order_id,item[0],item[1]))
            
        confirm_order()
            
    def on_back_click():
        root.destroy()
    
    
    submit_button = tk.Button(root,text="Place order",command=submit_order)
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
    order_label.grid(row=1, column=1,sticky='W')
    
    cursor.execute("{CALL dbo.ReadCustomerOrders (?)}",(cid))
    orders = cursor.fetchall()
    listbox = tk.Listbox(root, width=100, selectmode = 'single')
    for order in orders:
        date = str(order[1])
        ship_date = str(order[3])
        order_string = "    {},    {},    {},    {}".format(order[0],date,order[2],ship_date)
        listbox.insert(tk.END, order_string)
    listbox.grid(row=2, column=1)
  
    
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
        cursor.execute("{CALL dbo.ReadSpecificOnOrder (?)}", (selected_order()))
        details = cursor.fetchall()
        for detail in details:
            price = str(detail[4])
            detail_string = "    {},    {},    {},    {},    ${}".format(detail[0],detail[1],detail[2],detail[3],price)
            details_listbox.insert(tk.END, detail_string)
        

    display_details = tk.Button(root, text='details', command=show_details)
    display_details.grid(row=3, column=1)
    
    detail_label = tk.Label(root, text="Order Number, Product Number, Product Name, Amount, Price", font=("TkDefaultFont", 10))
    detail_label.grid(row=4, column=1,sticky='W')
    
    details_listbox = tk.Listbox(root, width=100, selectmode = 'single')
    details_listbox.grid(row=5, column=1)
    
   
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
register.grid(row=5,column=15, columnspan=5)

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




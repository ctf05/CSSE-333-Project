import tkinter as tk
import pyodbc


def main():
    conn = connect("titan.csse.rose-hulman.edu", "OneProduct", "SodaBaseUserbeadlich", "Password123")
    execute_stored_procedure(conn)


def connect(server, database, username, password):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return conn

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



def execute_stored_procedure(conn):
    #connect to the SQL Server instance
    cursor = conn.cursor()
    # call the stored procedure and pass the values of the dropdown menus as parameters
    cursor.execute("EXEC dbo.addCustomer @param1 = ?, @param2 = ?, @param3 = ?, @param4 = ?, @param5 = ?", ("fname", "lname", "123-5465-343", "jonesville", None))
    # retrieve the results of the stored procedure
    results = cursor.fetchall()
    # close the connection to the SQL Server instance
    cursor.close()
    conn.close()
    return results
main()
root.mainloop()

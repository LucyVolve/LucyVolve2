def login():
    from main import main_screen
    global login_screen
    global email_entry
    global password_entry
    login_screen = Toplevel (main_screen)
    login_screen.title("Login")
    login_screen.geometry("600x500")

    email = Stringvar()
    password = Stringvar()

    Label (login_screen, text = "Please enter the following details", bg = "red",)
    email_label = Label (login_screen, text = "Email * ")
    email_label.pack ()
    email_entry = Entry(login_screen, textvariable=email)
    email_entry.pack()
    password_label = Label(login_screen, text = "Password * ")
    password_label.pack()
    password_entry = Entry (login_screen, textvariable = password)

    Button(login_screen, text="Login", bg = "green", command=login_verify)

    def login_verify(password):
        email_info = email_entry.get()
        password_info = password_entry.get()

        encode_password = bcrypt.checkpw(password_info.encode('utf-8'), password.encode('utf-8'))

        conn = connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM user acct WHERE email = %s AND password = %s;
            """, (email_info, encode_password)
        )
        result = cur.fetchone()

        conn.close()

        if result:
            login_success()
        elif result == False:
            password_invalid()
        else:
            user_not_found()
def login_success():
    global login_success_screen
    login_success_screen = Toplevel (login_screen)
    login_screen_screen.title("success")
    login_success_screen.geometry("150x100")

    Label(login_success_screen, text="Login successfully", fg = "green", font= ("Calibri", 13)).pack()
    Button(login_success_screen, text='OK').pack()

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Failed")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text= "User not found", fg = "red", font=("Calibri", 13)).pack()
    Button(user_not_found_screen, text="OK", bg = "rdd", command=delete_user_not_found)   

def delete_user_not_found():
    user_not_found_screen.destroy()

def password_invalid():
    global password_invalid_screen
    password_invalid_screen = Toplevel(login_screen)
    password_invalid_screen.title("password")
    password_invalid_screen.goemetry("150x100")
    Label(password_invalid_screen, text="Password is invalid", fg="red", font=("Calibri", 13)).pack()
    Button(password_invalid_screen, text="OK", bg="red", command=delete_password_invalid)

def delete_password_invalid():
    password_invalid_screen.destroy()

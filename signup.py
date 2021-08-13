import tkinter as tk
from tkinter import *
import mysql.connector
import re
from tkinter import messagebox


def register():

    myconn = mysql.connector.connect(
        host='localhost', user='root', password='', database='real_estate')
    my_cursor = myconn.cursor()

    if myconn.is_connected():
        print('Connected to MySQL database')

    name1 = name.get()
    middle_name1 = Middle_name.get()
    surname1 = Surname.get()
    email1 = mail_Id.get()
    password1 = Password.get()
    confirm_pass = cpass.get()
    isvalid_email = check_email(email1)

    if name1 == '' or middle_name1 == '' or surname1 == '' or email1 == '' or password1 == '':
        messagebox.showinfo("showinfo", "Please fill the empty details")
    elif(isvalid_email == False):
        messagebox.showinfo("showinfo", "Please Enter a valid email-id")
    elif(confirm_pass != password1):
        messagebox.showinfo("showinfo", "Password does not match")
    elif password1:

        isvalid = validatepass(password1)
        print(isvalid)
        if(isvalid == False):
            messagebox.showerror(
                "showinfo", "Password should contain atleast one special character,one character,one number and lenght should be greater than 8")
        elif(name1.isdigit() or middle_name1.isdigit() or surname1.isdigit()):
            messagebox.showerror(
                "showinfo", "Name should not be a digit!")
        else:
            sql = "select * from user where mail = %s and Password = %s"
            check = (email1, password1)
            my_cursor.execute(sql, check)
            results = my_cursor.fetchall()
            if(results):
                messagebox.showerror("showerror", "Account already exists!")
            else:
                my_cursor.execute("INSERT INTO `user`(`Fname`, `Mname`, `Lname`, `mail`, `Password`) VALUES (%s,%s,%s,%s,%s);",
                                  (name1, middle_name1, surname1, email1, password1,))
                messagebox.showinfo("showinfo", "Stored successfully")
                myconn.commit()

    my_cursor.close()
    myconn.close()


def check_email(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        print("Valid Email")
        return True
    else:
        return False


def validatepass(passw):
    fl = 0

    while True:
        print(len(passw))
        if (len(passw) < 8):
            fl = -1
            break
        elif not re.search("[a-z]", passw):
            fl = -1
            break
        elif not re.search("[A-Z]", passw):
            fl = -1
            break
        elif not re.search("[0-9]", passw):
            fl = -1
            break
        elif not re.search("[_@$]", passw):
            fl = -1
            break
        elif re.search("\s", passw):
            fl = -1
            break
        else:
            fl = 0
            break
    if(fl == 0):
        return True
    else:
        return False


def registration():
    global window
    window = tk.Tk()

    global name
    global Middle_name
    global Surname
    global mail_Id
    global Password
    global cpass

    name = StringVar()
    Middle_name = StringVar()
    Surname = StringVar()
    mail_Id = StringVar()
    Password = StringVar()
    cpass = StringVar()
    message = StringVar()

    window.geometry('500x500')
    window['bg'] = '#a3d2fb'
    window.title('Signup Page')
    label = tk.Label(window, text='CREATE ACCOUNT', width=20, bg="#a3d2fb",
                     font=('Bold', 20)).place(x=90, y=53)

    label1 = tk.Label(window, text='Name :', width=20, bg="#a3d2fb",
                      font=('bold', 10)).place(x=80, y=130)
    entry1 = tk.Entry(window, textvariable=name).place(x=240, y=130)

    label2 = tk.Label(window, text='Middle name :', width=20, bg="#a3d2fb",
                      font=('bold', 10)).place(x=70, y=180)
    entry = tk.Entry(window, textvariable=Middle_name).place(x=240, y=180)

    label3 = tk.Label(window, text=' Surname :', width=20, bg="#a3d2fb",
                      font=('bold', 10)).place(x=60, y=230)
    entry3 = tk.Entry(window, textvariable=Surname).place(x=240, y=230)

    label4 = tk.Label(window, text=' E-mail Id :', width=20, bg="#a3d2fb",
                      font=('bold', 10)).place(x=50, y=280)
    entry4 = tk.Entry(window, textvariable=mail_Id).place(x=240, y=280)

    label5 = tk.Label(window, text=' Password :', width=20, bg="#a3d2fb",
                      font=('bold', 10)).place(x=60, y=330)
    entry5 = tk.Entry(window, show='*',
                      textvariable=Password).place(x=240, y=330)

    label5 = tk.Label(window, text='Confirm password :', bg="#a3d2fb",
                      width=20, font=('bold', 10)).place(x=60, y=380)
    entry5 = tk.Entry(window, show='*', textvariable=cpass).place(x=240, y=380)

    button1 = tk.Button(window, text='Register',
                        command=register).place(x=180, y=430)
    button2 = tk.Button(window, text='Cancel',
                        command=window.quit).place(x=280, y=430)

    window.mainloop()


registration()

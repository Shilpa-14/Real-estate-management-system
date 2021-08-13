from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from home import homepg
import re


class Userlogin():
    def __init__(self, window):
        self.window = window
        self.window['bg'] = '#a3d2fb'
        self.islogged = False
        self.window.geometry('500x500')
        self.window.title('login Page')
        self.email = StringVar()
        self.password = StringVar()
        label = Label(self.window, text='LOGIN TO ACCOUNT', bg='#a3d2fb',
                      width=20, font=('Bold', 20))
        label.place(x=70, y=80)

        label1 = Label(self.window, text='E-mail :', width=20, bg='#a3d2fb',
                       font=('bold', 10))
        label1.place(x=70, y=130)
        self.entry1 = Entry(self.window)
        self.entry1.place(x=240, y=130)

        label2 = Label(self.window, text='Password :', width=20, bg='#a3d2fb',
                       font=('bold', 10))
        label2.place(x=70, y=180)
        self.entry = Entry(self.window, show='*')
        self.entry.place(x=240, y=180)

        button1 = tk.Button(self.window, text='Login', width=20,
                            command=self.loginuser).place(x=160, y=230)

    def loginuser(self):
        global username
        myconn = mysql.connector.connect(
            host='localhost', user='root', password='', database='real_estate')
        mycursor = myconn.cursor()
        mail_verify = self.entry1.get()
        pass_verify = self.entry.get()
        sql = "select * from user where mail = %s and Password = %s"
        check = (mail_verify, pass_verify)
        mycursor.execute(sql, check)
        results = mycursor.fetchall()

        if results:
            for row in results:
                messagebox.showinfo("showinfo", "SUCCESSFULLY LOGGED IN ")
                username = row[0]
                uid = row[4]
                root = tk.Tk()
                obj = homepg(root, username, uid)
                break
        else:
            messagebox.showinfo("showinfo", "please add valid details")
            self.islogged = False


window = tk.Tk()
l = Userlogin(window)
window.mainloop()

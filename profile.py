from tkinter import *
import tkinter as tk
from tkinter import ttk
import mysql.connector
from form import Form
from PIL import Image, ImageTk
from tkinter import messagebox
import smtplib
import os
from email.mime.text import MIMEText


class Profilepg:
    def __init__(self, root, username, uid):
        self.root = root
        self.uid = uid
        self.username = username
        self.root.title("My profile")
        self.root.geometry("1000x500")
        self.root['bg'] = '#a3d2fb'
        self.plotinfo = {}
        self.clear_count = 0
        self.prev_plotcount = 0
        self.entryframe = Frame(self.root)
        self.entryframe.pack()

        self.db = mysql.connector.connect(
            host="localhost", user="root", password="", db="real_estate")
        self.cursor = self.db.cursor()

        self.plot_type = Label(self.entryframe, text="Select Plot type", font=(
            "times new roman", 15, "bold"), fg="black")
        self.e = ttk.Combobox(self.entryframe, width=15, height=15)
        self.e['values'] = ("Select", "Building", "Bungalow", "Plot")
        self.plot_type.pack(side=LEFT)
        self.e.pack(side=LEFT)

        search = Button(self.entryframe, text='Search',
                        width=15, height=2, command=self.getitems)
        search.pack(side=LEFT)

        Form = Button(self.entryframe, text='Form', width=15,
                      height=2, command=self.formfill)
        Form.pack(side=LEFT)

        clrbtn = Button(self.entryframe, text='clear', width=15,
                        height=2, command=self.clearframe)
        clrbtn.pack(side=LEFT)

        self.canvas = tk.Canvas(self.root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda event,
                        canvas=self.canvas: self.onFrameConfigure(self.canvas))

        # self.plotframe = Frame(self.frame, width=30, height=100, bg="#a3d2fb")

    def onFrameConfigure(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def formfill(self):
        root = Tk()
        obj = Form(root, self.uid)

    def getitems(self):
        if self.e.get() == "" or self.e.get() == "Select":
            messagebox.showerror(
                "Error", "Select a plot type", parent=self.root)
        uid = 1
        sqlstatement = "SELECT * FROM saveditems where save_user_id=" + \
            f'{self.uid}'
        self.cursor.execute(sqlstatement)
        res = self.cursor.fetchall()
        print(res)
        if(self.e.get() == 'Bungalow'):
            flag = False
            i = 0
            for row in res:
                if(row[3] != None):
                    sql1 = """SELECT * FROM  bunglow where Bung_id=%s"""
                    self.cursor.execute(sql1, (row[3],))
                    res1 = self.cursor.fetchall()
                    for row in res1:
                        plotinfosubdict = {}
                        i = i+1
                        plotinfosubdict['name'] = row[1]
                        plotinfosubdict['address'] = row[2]
                        plotinfosubdict['room'] = row[3]
                        plotinfosubdict['price'] = row[4]
                        plotinfosubdict['sqft'] = row[5]
                        self.plotinfo[i] = plotinfosubdict
                        flag = True
            if flag == False:
                plotframe = Frame(self.frame, width=50,
                                  height=100, bg="#FFE4B5")
                plotframe.grid(row=1, column=1, padx=5, pady=10)
                s = Message(plotframe, text="You have no saved items in Bungalows",
                            width=500, bg="#FFE4B5").grid(row=3, column=2)

        if(self.e.get() == 'Building'):
            flag = False
            i = 0
            for row in res:
                print(row)
                if(row[4] != None):
                    sql1 = """SELECT * FROM  Building where Build_id=%s"""
                    self.cursor.execute(sql1, (row[4],))
                    res1 = self.cursor.fetchall()
                    for row in res1:
                        plotinfosubdict = {}
                        i = i+1
                        plotinfosubdict['name'] = row[1]
                        plotinfosubdict['address'] = row[2]
                        plotinfosubdict['room'] = row[3]
                        plotinfosubdict['price'] = row[4]
                        plotinfosubdict['sqft'] = row[5]
                        self.plotinfo[i] = plotinfosubdict
                        flag = True
            if flag == False:
                plotframe = Frame(self.frame, width=50,
                                  height=100, bg="#FFE4B5")
                plotframe.grid(row=1, column=1, padx=5, pady=10)
                s = Message(plotframe, text="You have no saved items in Buildings", font=("Times new Roman", 30),
                            width=500, bg="#FFE4B5").grid(row=3, column=2)

        if(self.e.get() == 'Plot'):
            flag = False
            i = 0
            for row in res:
                if(row[2] != None):
                    sql1 = """SELECT * FROM  plot where P_id=%s"""
                    self.cursor.execute(sql1, (row[2],))
                    res1 = self.cursor.fetchall()
                    for row in res1:
                        plotinfosubdict = {}
                        i = i+1
                        plotinfosubdict['name'] = row[1]
                        plotinfosubdict['address'] = row[2]
                        plotinfosubdict['room'] = 'No rooms'
                        plotinfosubdict['price'] = row[4]
                        plotinfosubdict['sqft'] = row[3]
                        self.plotinfo[i] = plotinfosubdict
                        flag = True
            if flag == False:
                plotframe = Frame(self.frame, width=50,
                                  height=100, bg="#FFE4B5")
                plotframe.grid(row=1, column=1, padx=300, pady=10)
                s = Message(plotframe, text="You have no saved items in Plots!!", width=500,
                            bg="#FFE4B5", font=("Times new Roman", 30)).grid(row=3, column=2,)

        self.populate()

    def save_entry(self, btn, plotname):
        y = str(btn)
        z = y[22]
        if(self.clear_count == 1):
            if(z == '.'):
                z = 1
            else:
                z = int(y[22])
            id = z - self.prev_plotcount
        elif(self.clear_count >= 2):
            if(y[23].isdigit()):
                print(y[23])
                z = y[22:24]
                z = int(z)
            else:
                z = int(y[22])
            id = z - self.prev_plotcount
        else:
            if(z == '.'):
                z = 1
            else:
                z = int(y[22])
            id = z
        print("id = ", id)
        f_id = self.plotinfo[id]['id']
        print("final id = ", f_id)
        if(self.e3.get() == 'Bungalow'):
            try:
                sql1 = 'INSERT INTO `saveditems`(`save_user_id`, `save_bung_id`) VALUES (%s,%s)'
                self.cursor.execute(sql1, (self.uid, f_id,))
                self.db.commit()
                messagebox.showinfo('show info', 'Saved Successfully')
            except TypeError:
                messagebox.showerror('show info', 'Sorry! some error occured')

    def view_entry(self, btn_name):
        print(btn_name)
        y = str(btn_name)
        z = y[22]
        if(self.clear_count == 1):
            if(z == '.'):
                z = 1
            else:
                z = int(y[22])
            id = z - self.prev_plotcount
        elif(self.clear_count >= 2):
            if(y[23].isdigit()):
                print(y[23])
                z = y[22:24]
                z = int(z)
            else:
                z = int(y[22])
            id = z - self.prev_plotcount
        else:
            if(z == '.'):
                z = 1
            else:
                z = int(y[22])
            id = z
        print("id = ", id)
        f_id = self.plotinfo[id]['id']
        print(f_id)
        if(self.e3.get() == 'Bungalow'):
            try:
                subdir = 'bung_imgid'+f'{f_id}'
                list = os.listdir('./imageinput/'+subdir)
                root1 = Tk()
                for i in range(len(list)):
                    print(i)
                    my_img = Image.open(
                        './imageinput/'+subdir+'/'+f'{i+1}'+'.PNG')
                    my_img = my_img.resize((200, 200), Image.ANTIALIAS)
                    image = ImageTk.PhotoImage(master=root1, image=my_img)
                    label = Label(root1, image=image)
                    label.photo = image
                    label.grid(row=0, column=i)
                root1.mainloop()
            except:
                print('No images found')
        elif(self.e3.get() == 'Building'):
            try:
                subdir = 'build_imgid'+f'{f_id}'
                list = os.listdir('./imageinput/'+subdir)
                root1 = Tk()
                for i in range(len(list)):
                    print(i)
                    my_img = Image.open(
                        './imageinput/'+subdir+'/'+f'{i+1}'+'.PNG')
                    my_img = my_img.resize((200, 200), Image.ANTIALIAS)
                    image = ImageTk.PhotoImage(master=root1, image=my_img)
                    label = Label(root1, image=image)
                    label.photo = image
                    label.grid(row=0, column=i)
                root1.mainloop()
            except TypeError:
                print('No images found')
        elif(self.e3.get() == 'Plot'):
            try:
                subdir = 'plot_imgid'+f'{f_id}'
                list = os.listdir('./imageinput/'+subdir)
                root1 = Tk()
                for i in range(len(list)):
                    print(i)
                    my_img = Image.open(
                        './imageinput/'+subdir+'/'+f'{i+1}'+'.PNG')
                    my_img = my_img.resize((200, 200), Image.ANTIALIAS)
                    image = ImageTk.PhotoImage(master=root1, image=my_img)
                    label = Label(root1, image=image)
                    label.photo = image
                    label.grid(row=0, column=i)
                root1.mainloop()
            except TypeError:
                print('No images found')

    def enquire_entry(self, btn_name):
        y = str(btn_name)
        z = y[22]
        if(self.clear_count == 1):
            if(z == '.'):
                z = 1
            else:
                z = int(y[22])
            id = z - self.prev_plotcount
        elif(self.clear_count >= 2):
            if(y[23].isdigit()):
                print(y[23])
                z = y[22:24]
                z = int(z)
            else:
                z = int(y[22])
            id = z - self.prev_plotcount
        else:
            if(z == '.'):
                z = 1
            else:
                z = int(y[22])
            id = z
        print("id = ", id)
        f_id = self.plotinfo[id]['id']
        print("final id=", f_id)
        self.cursor.execute(
            "Select mail from user where user_id=" + f'{self.uid}')
        res = self.cursor.fetchall()
        for row in res:
            print(row)
            mail = row[0]

        if(self.e3.get() == 'Bungalow'):
            sql1 = 'SELECT owner_detail FROM `bunglow` WHERE Bung_id =' + \
                f'{f_id}'
            self.cursor.execute(sql1)
            res = self.cursor.fetchall()
            for row in res:
                print(row)
                owner_no = row[0]
        elif(self.e3.get() == 'Building'):
            sql1 = 'SELECT owner_detail FROM `building` WHERE Build_id =' + \
                f'{f_id}'
            self.cursor.execute(sql1)
            res = self.cursor.fetchall()
            for row in res:
                print(row)
                owner_no = row[0]
        elif(self.e3.get() == 'Plot'):
            sql1 = 'SELECT owner_detail FROM `bunglow` WHERE Bung_id =' + \
                f'{f_id}'
            self.cursor.execute(sql1)
            res = self.cursor.fetchall()
            for row in res:
                print(row)
                owner_no = row[0]

        body = 'Hello '+self.username+',<br>Your appointment is booked successfully.please call on: ' + \
            owner_no + 'for further details...'

        # make up message
        msg = MIMEText(body)
        msg['Subject'] = 'Appointment booked'
        msg['From'] = "realestate.mp2001@gmail.com"
        msg['To'] = mail
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login("realestate.mp2001@gmail.com", "1234@&**")
            server.sendmail("realestate.mp2001@gmail.com",
                            mail, msg.as_string())
            server.close()
            messagebox.showinfo('show info', 'Email has been sent')
        except:
            print("failed to send mail")
            messagebox.showerror(
                'show info', 'Sorry,There was some issue!,try again later')

    def populate(self):
        for i in range(len(self.plotinfo)):
            if(i < 3):
                row = 0
                column = i
            elif(3 <= i < 6):
                row = 1
                column = i - 3
            elif(6 <= i < 9):
                row = 2
                column = i - 3
            plotframe = Frame(self.frame, width=30, height=100, bg="#FFE4B5")
            plotframe.grid(row=row, column=column, padx=5, pady=10)
            # adding plotname,rooms,price
            pname = Message(plotframe, text="Name:"+self.plotinfo[i+1]['name'], width=200,
                            bg="#FFE4B5").grid(row=0)
            paddr = Message(plotframe, text="Address: "+self.plotinfo[i+1]['address'], width=250,
                            bg="#FFE4B5").grid(row=1)
            pprice = Message(plotframe, text="price = "+self.plotinfo[i+1]['price'], width=150,
                             bg="#FFE4B5").grid(row=2)
            prooms = Message(plotframe, text="No. of rooms= "+str(self.plotinfo[i+1]['room']), width=150,
                             bg="#FFE4B5").grid(row=3)
            psqft = Message(plotframe, text="Sq. ft area= "+str(self.plotinfo[i+1]['sqft']), width=150,
                            bg="#FFE4B5").grid(row=4)

            # view button
            viewbtn = Button(plotframe, text='view', width=8, height=1)
            viewbtn.configure(
                command=lambda button=viewbtn: self.view_entry(button))
            viewbtn.grid(row=5, column=0, padx=5, pady=10)

            # save button
            savebtn = Button(plotframe, text='Save', width=8, height=1)
            savebtn.configure(
                command=lambda button=savebtn: self.save_entry(button))
            savebtn.grid(row=5, column=1, padx=5, pady=10)
            # enquire button
            enquirebtn = Button(plotframe, text='Enquire', width=8, height=1)
            enquirebtn.configure(
                command=lambda button=enquirebtn: self.enquire_entry(button))
            enquirebtn.grid(row=5, column=2, padx=5, pady=10)

    def clearframe(self):
        self.clear_count = self.clear_count+1
        self.prev_plotcount = self.prev_plotcount + len(self.plotinfo)
        for widget in self.frame.winfo_children():
            widget.destroy()
        for i in range(len(self.plotinfo)):
            del self.plotinfo[i+1]
        print(self.plotinfo)


# root = Tk()
# obj = Profilepg(root)
# root.mainloop()


if(__name__ == '__main__'):
    root.mainloop()

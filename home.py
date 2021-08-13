import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import mysql.connector
from profile import Profilepg
from tkinter import messagebox
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText


class homepg():

    def __init__(self, root, username, uid):
        self.root = root
        self.root.geometry("800x800")
        self.root['bg'] = '#a3d2fb'
        self.username = username
        self.uid = uid
        self.clear_count = 0
        self.prev_plotcount = 0
        print("user=====", self.username)
        self.areadict = {}
        self.plotinfo = {}

        # making connection
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="", db="real_estate")
        self.cursor = self.db.cursor()

        # making heading
        Message(self.root, text='Let us Guide you Home', width=400,
                font=('Roman', 30, 'bold'), fg='#12528a', bg='#a3d2fb').pack()

        # Create a photoimage object of the image in the path

        image1 = Image.open("./homeimg.png")
        image1 = image1.resize((1200, 200), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(master=self.root, image=image1)
        label1 = Label(self.root, image=test, bg='#a3d2fb')
        label1.image = test
        # Position image
        label1.pack()

        # making frame for custom menubar
        self.menuframe = Frame(self.root)
        self.menuframe.pack()
        self.entryframe = Frame(self.root)
        self.entryframe.pack()
        self.btnframe = Frame(self.root)
        self.btnframe.pack()

        # variables
        self.Area = tk.StringVar()
        self.City = tk.StringVar()
        self.plotType = tk.StringVar()
        self.mode = tk.StringVar()

        # menubar
        Label(self.menuframe, text='        Area         ',
              font=('Arial', 14)).pack(side=LEFT)
        Label(self.menuframe, text='        City        ',
              font=('Arial', 14)).pack(side=LEFT)
        Label(self.menuframe, text='        Plot type        ',
              font=('Arial', 14)).pack(side=LEFT)
        Label(self.menuframe, text='        mode       ',
              font=('Arial', 14)).pack(side=LEFT)
        self.e1 = Entry(self.entryframe, textvariable=self.Area)
        self.e2 = ttk.Combobox(self.entryframe, width=10)
        self.e3 = ttk.Combobox(self.entryframe, width=10)
        self.e3['values'] = ("Building", "Bungalow", "Plot")
        self.e2['values'] = ("Kalyan", "Dombivli", "Thane", "Kurla", "Dadar", "Byculla",
                             "Nahur", "Bhandup", "Mulund", "Ghatkopar")
        self.e4 = ttk.Combobox(self.entryframe, width=10)
        self.e4['values'] = ("rent", "sale")
        self.e1.pack(side=LEFT)
        self.e2.pack(side=LEFT)
        self.e3.pack(side=LEFT)
        self.e4.pack(side=LEFT)
        # search button
        searchbtn = Button(self.btnframe, text='Search', width=15,
                           height=2, command=self.search)
        searchbtn.pack(side=LEFT)

        # Myprofile button
        profilebtn = Button(self.btnframe, text='My Profile', width=15,
                            height=2, command=self.Myprofile)
        profilebtn.pack(side=LEFT)

        # clear
        clrbtn = Button(self.btnframe, text='clear', width=15,
                        height=2, command=self.clearframe)
        clrbtn.pack(side=LEFT)
        m = Message(self.btnframe, text='Hello '+self.username, width=400,
                    font=('Helvetica', 15, 'bold'), fg='#12528a', bg='#a3d2fb')
        m.pack(side=LEFT)

        self.canvas = tk.Canvas(self.root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(
            self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda event,
                        canvas=self.canvas: self.onFrameConfigure(self.canvas))

    def search(self):
        area_name = self.e1.get()
        print("area name:", area_name)
        city_name = self.e2.get()
        plot_type = self.e3.get()
        b_mode = self.e4.get()
        area_no = 0
        city_no = 0
        if((city_name == '' or plot_type == '' or b_mode == '') and (area_name == '' or plot_type == '' or b_mode == '')):
            if(city_name == '' and area_name == ''):
                messagebox.showerror(
                    'show info', 'Please Either enter city or area')
            elif(plot_type == '' or b_mode == ''):
                messagebox.showerror(
                    'show info', 'Please enter all fields')
        else:
            if(area_name):
                try:
                    sql1 = "SELECT area_no FROM area WHERE Area_name = '"+area_name+"'"
                    self.cursor.execute(sql1)
                    area_no = self.cursor.fetchone()[0]
                except TypeError:
                    area_no = 0
                    messagebox.showerror('show info', 'No results found')
            elif(city_name):
                try:
                    sql2 = "SELECT city_no FROM city WHERE city_name = '"+city_name+"'"
                    self.cursor.execute(sql2)
                    city_no = self.cursor.fetchone()[0]
                except:
                    city_no = 0
                    messagebox.showerror('show info', 'No results found')
            else:
                messagebox.showerror('show info', 'No results found')
        self.getplots(area_no, city_no, city_name, plot_type, b_mode)

    def Myprofile(self):
        root = Tk()
        obj = Profilepg(root, self.username, self.uid)

    def onFrameConfigure(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def getplots(self, area_no, city_no, city_name, plot_type, b_mode):
        if(area_no != 0):
            if(self.e3.get() == 'Bungalow'):
                sql1 = "SELECT * FROM `bunglow`" + \
                    " WHERE bung_area_no = " + \
                    f'{area_no}' + " AND type = '"+b_mode + "'"
                self.cursor.execute(sql1)
                res = self.cursor.fetchall()
                i = 0
                for row in res:
                    print("row===", row)
                    plotinfosubdict = {}
                    i = i+1
                    plotinfosubdict['id'] = row[0]
                    plotinfosubdict['name'] = row[1]
                    plotinfosubdict['address'] = row[2]
                    plotinfosubdict['room'] = row[3]
                    plotinfosubdict['price'] = row[4]
                    plotinfosubdict['sqft'] = row[5]
                    self.plotinfo[i] = plotinfosubdict
            elif(self.e3.get() == 'Building'):
                sql1 = "SELECT * FROM `building`" + \
                    " WHERE area_no = "+f'{area_no}' + \
                    " AND type = '"+b_mode+"'"
                self.cursor.execute(sql1)
                res = self.cursor.fetchall()
                i = 0
                for row in res:
                    plotinfosubdict = {}
                    i = i+1
                    plotinfosubdict['id'] = row[0]
                    plotinfosubdict['name'] = row[1]
                    plotinfosubdict['address'] = row[2]
                    plotinfosubdict['room'] = row[3]
                    plotinfosubdict['price'] = row[4]
                    plotinfosubdict['sqft'] = row[5]
                    self.plotinfo[i] = plotinfosubdict
            elif(self.e3.get() == 'Plot'):
                flag = False
                sql1 = "SELECT * FROM `plot`" + \
                    " WHERE Plot_area_no = " + \
                    f'{area_no}' + " AND type = '"+b_mode + "'"
                self.cursor.execute(sql1)
                res = self.cursor.fetchall()
                i = 0
                for row in res:
                    plotinfosubdict = {}
                    i = i+1
                    plotinfosubdict['id'] = row[0]
                    plotinfosubdict['name'] = row[1]
                    plotinfosubdict['address'] = row[2]
                    plotinfosubdict['sqft'] = row[3]
                    plotinfosubdict['price'] = row[4]
                    self.plotinfo[i] = plotinfosubdict
            else:
                messagebox.showerror('show info', 'Enter a valid plot type')
        else:
            sql3 = "SELECT area_no FROM area WHERE city_no = "+f'{city_no}'
            self.cursor.execute(sql3)
            res = self.cursor.fetchall()
            i = 0
            y = 0
            for row1 in res:
                print(row1)
                if(self.e3.get() == 'Bungalow'):
                    flag = False
                    sql1 = "SELECT * FROM `bunglow`WHERE bung_area_no = " + \
                        f'{row1[0]}' + " AND type = '"+b_mode + "'"
                    self.cursor.execute(sql1)
                    res = self.cursor.fetchall()
                    for row in res:
                        print("row===", row)

                        plotinfosubdict = {}
                        i = i+1
                        plotinfosubdict['id'] = row[0]
                        plotinfosubdict['name'] = row[1]
                        plotinfosubdict['address'] = row[2]
                        plotinfosubdict['room'] = row[3]
                        plotinfosubdict['price'] = row[4]
                        plotinfosubdict['sqft'] = row[5]
                        self.plotinfo[i] = plotinfosubdict
                    print(self.plotinfo)
                elif(self.e3.get() == 'Building'):
                    flag = False
                    sql1 = "SELECT * FROM `building" + \
                        "` WHERE area_no = " + \
                        f'{row1[0]}' + " AND type = '"+b_mode + "'"
                    self.cursor.execute(sql1)
                    res = self.cursor.fetchall()
                    i = 0
                    for row in res:

                        plotinfosubdict = {}
                        i = i+1
                        plotinfosubdict['id'] = row[0]
                        plotinfosubdict['name'] = row[1]
                        plotinfosubdict['address'] = row[2]
                        plotinfosubdict['room'] = row[3]
                        plotinfosubdict['price'] = row[4]
                        plotinfosubdict['sqft'] = row[5]
                        self.plotinfo[i] = plotinfosubdict
                        flag = True
                elif(self.e3.get() == 'Plot'):
                    sql1 = "SELECT * FROM `plot" + \
                        "` WHERE Plot_area_no = " + \
                        f'{row1[0]}' + " AND type = '"+b_mode + "'"
                    self.cursor.execute(sql1)
                    res = self.cursor.fetchall()
                    i = 0
                    for row in res:
                        plotinfosubdict = {}
                        i = i+1
                        plotinfosubdict['id'] = row[0]
                        plotinfosubdict['name'] = row[1]
                        plotinfosubdict['address'] = row[2]
                        plotinfosubdict['sqft'] = row[3]
                        plotinfosubdict['price'] = row[4]
                        self.plotinfo[i] = plotinfosubdict
                else:
                    messagebox.showerror(
                        'show info', 'Enter a valid plot type')
                y = y+1
        self.populate()

        def save_entry(self, btn):
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
                    messagebox.showerror(
                        'show info', 'Sorry! some error occured')

    def save_entry(self, btn):
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
                messagebox.showinfo(
                    'showinfo', 'Sorry No images are available')
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
                messagebox.showinfo(
                    'showinfo', 'Sorry No images are available')
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
                messagebox.showinfo(
                    'showinfo', 'Sorry No images are available')

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

        body = 'Hello '+self.username+',Your appointment is booked successfully.please call on: ' + \
            owner_no + ' for further details...'

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
        column = 0

        '''Put in some fake data'''
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
            self.plotframe = Frame(self.frame, width=30,
                                   height=100, bg="#a3d2fb")
            self.plotframe.grid(row=row, column=column, padx=5, pady=10)
            # adding plotname,rooms,price
            pname = Message(self.plotframe, text="Name: ",
                            bg="#a3d2fb").grid(row=0, column=0)
            pname1 = Message(self.plotframe, text=''+self.plotinfo[i+1]['name'], width=100,
                             bg="#a3d2fb").grid(row=0, column=1)
            paddr = Message(self.plotframe, text="Address: ", width=100,
                            bg="#a3d2fb").grid(row=1, column=0)
            paddr1 = Message(self.plotframe, text=""+self.plotinfo[i+1]['address'], width=100,
                             bg="#a3d2fb").grid(row=1, column=1)
            pprice = Message(self.plotframe, text="price: ",
                             bg="#a3d2fb").grid(row=2, column=0)
            pprice1 = Message(self.plotframe, text=""+self.plotinfo[i+1]['price'],
                              bg="#a3d2fb").grid(row=2, column=1)
            if('rooms' in self.plotinfo[i+1]):
                prooms = Message(self.plotframe, text="No. of rooms: ",
                                 bg="#a3d2fb").grid(row=3, column=0)
                prooms1 = Message(self.plotframe, text="No. of rooms: "+self.plotinfo[i+1]['room'],
                                  bg="#a3d2fb").grid(row=3, column=1)
            else:
                pass
            psqft = Message(self.plotframe, text="Sq.ft area: ",
                            bg="#a3d2fb").grid(row=4, column=0)
            psqft = Message(self.plotframe, text="" + self.plotinfo[i+1]['sqft'],
                            bg="#a3d2fb").grid(row=4, column=1)

            # view button
            viewbtn = Button(self.plotframe, text='view', width=8, height=1)
            viewbtn.configure(
                command=lambda button=viewbtn: self.view_entry(button))
            viewbtn.grid(row=5, column=0, padx=5, pady=10)

            # save button
            savebtn = Button(self.plotframe, text='Save', width=8, height=1)
            savebtn.configure(
                command=lambda button=savebtn: self.save_entry(button))
            savebtn.grid(row=5, column=1, padx=5, pady=10)
            # enquire button
            enquirebtn = Button(
                self.plotframe, text='Enquire', width=8, height=1)
            enquirebtn.configure(
                command=lambda button=enquirebtn: self.enquire_entry(button))
            enquirebtn.grid(row=5, column=2, padx=5, pady=10)
            # column = column+1
        if(len(self.plotinfo) == 0):
            self.plotframe = Frame(self.frame, width=50,
                                   height=100, bg="#a3d2fb")
            self.plotframe.grid(row=1, column=1, padx=300, pady=10)
            s = Message(self.plotframe, text="No results found", width=500,
                        bg="#a3d2fb", font=("Times new Roman", 30)).grid(row=3, column=2,)

    def clearframe(self):
        self.clear_count = self.clear_count+1
        self.prev_plotcount = self.prev_plotcount + len(self.plotinfo)
        for widget in self.frame.winfo_children():
            widget.grid_forget()
        for i in range(len(self.plotinfo)):
            del self.plotinfo[i+1]

        print(self.plotinfo)


if(__name__ == "__main__"):
    root.mainloop()
# root = Tk()
# obj = homepg(root, 'Aditi', 2)
# root.mainloop()

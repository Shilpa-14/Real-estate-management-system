from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import os
import re
from tkinter import filedialog
from PIL import Image, ImageTk


class Form:
    def __init__(self, root, uid):
        self.root = root
        self.root.title("Form")
        self.root.geometry('1000x700+0+0')
        self.root.config(bg="#a3d2fb")
        self.uid = uid
        print("form uid=", self.uid)
        self.storepath = ""
        self.j = 1
        self.p = ""
        self.r = 0

        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="real_estate")
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM user WHERE user_id= %s""", (self.uid,))
        result3 = cur.fetchall()
        List = []
        for i in result3:
            print(i)
            self.fname = i[0]
            self.mname = i[1]
            self.lname = i[2]
            self.email = i[3]

        frame1 = Frame(self.root, bg="white")
        frame1.place(x=50, y=50, width=900, height=600)
        textEntry = StringVar(self.root, value=self.fname)
        # textEntry.set(self.setText(1))
        firstname = Label(frame1, text="Firstname", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=50, y=50)
        self.txt_firstname = Entry(frame1, font=(
            "times new Roman", 15), bg="lightgray", textvariable=textEntry, state='disabled')
        self.txt_firstname.place(x=50, y=80, width=250)

        textEntry2 = StringVar(self.root, value=self.mname)
        # textEntry2.set(self.setText(2))
        middlename = Label(frame1, text="Middlename", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=370, y=50)
        self.txt_middlename = Entry(frame1, font=(
            "times new Roman", 15), bg="lightgray", textvariable=textEntry2, state='disabled')
        self.txt_middlename.place(x=370, y=80, width=50)

        textEntry3 = StringVar(self.root, value=self.lname)
        # textEntry3.set(self.setText(3))
        lastname = Label(frame1, text="Lastname", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=580, y=50)
        self.txt_lastname = Entry(frame1, font=(
            "times new Roman", 15), bg="lightgray", textvariable=textEntry3, state='disabled')
        self.txt_lastname.place(x=580, y=80, width=250)

        textEntry4 = StringVar(self.root, value=self.email)
        # textEntry4.set(self.setText(4))
        email = Label(frame1, text="Email-id", font=("times new roman",
                      15, "bold"), bg="white", fg="black").place(x=50, y=130)
        self.txt_email = Entry(frame1, font=(
            "times new Roman", 15), bg="lightgray", textvariable=textEntry4, state='disabled')
        self.txt_email.place(x=50, y=160, width=250)

        plot_type = Label(frame1, text="Select plot type", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=370, y=130)
        self.cmb_plot_type = ttk.Combobox(
            frame1, font=("times new roman", 15, "bold"))
        self.cmb_plot_type['values'] = (
            "Select", "Building", "Bungalow", "Plot")
        self.cmb_plot_type.place(x=370, y=160, width=180)

        name = Label(frame1, text="Enter Building/Bungalow/Plot name", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=580, y=130)
        self.txt_name = Entry(frame1, font=(
            "times new Roman", 15), bg="lightgray")
        self.txt_name.place(x=580, y=160, width=250)

        city = Label(frame1, text="Enter City", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=50, y=240)
        self.txt_city = ttk.Combobox(
            frame1, font=("times new roman", 15, "bold"))
        self.txt_city['values'] = ("Kalyan", "Dombivli", "Thane", "Kurla", "Dadar", "Byculla",
                                   "Nahur", "Bhandup", "Mulund", "Ghatkopar")
        self.txt_city.place(x=50, y=270, width=250)

        No_of_rooms = Label(frame1, text="No of rooms", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=370, y=240)
        self.cmb_no_of_rooms = ttk.Combobox(
            frame1, font=("times new roman", 15, "bold"))
        self.cmb_no_of_rooms['values'] = ("Select", "1", "2", "3", "4", "5")
        self.cmb_no_of_rooms.place(x=370, y=270, width=180)

        locality = Label(frame1, text="Locality", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=580, y=240)
        self.txt_locality = Entry(frame1, font=(
            "times new Roman", 15), bg="lightgray")
        self.txt_locality.place(x=580, y=270, width=250)

        area = Label(frame1, text="Enter Area", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=50, y=320)
        self.txt_area = Entry(frame1, font=(
            "times new Roman", 15), bg="lightgray")
        self.txt_area.place(x=50, y=350, width=250)

        Type = Label(frame1, text="Type", font=("times new roman",
                     15, "bold"), bg="white", fg="black").place(x=370, y=320)
        self.cmb_type = ttk.Combobox(
            frame1, font=("times new roman", 15, "bold"))
        self.cmb_type['values'] = ("Select", "sale", "rent")
        self.cmb_type.place(x=370, y=350, width=180)

        price_range = Label(frame1, text="Price_range", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=580, y=320)
        self.txt_price_range = Entry(frame1, font=(
            "times new Roman", 15), bg="lightgray")
        self.txt_price_range.place(x=580, y=350, width=250)

        sq_ft = Label(frame1, text="Enter sq_ft", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=50, y=410)
        self.txt_sq_ft = Entry(frame1, font=(
            "times new Roman", 15), bg="lightgray")
        self.txt_sq_ft.place(x=50, y=440, width=250)

        phone_no = Label(frame1, text="Mobile number", font=(
            "times new roman", 15, "bold"), bg="white", fg="black").place(x=350, y=420)
        self.txt_phone_no = Entry(frame1, font=(
            "times new Roman", 15), bg="lightgray")
        self.txt_phone_no.place(x=350, y=450, width=230)

        upload_image = Button(frame1, text="Click here to add image", font=("times new roman", 15, "bold"),
                              bd=0, cursor="hand2", bg="gray", command=self.takeinput).place(x=600, y=430, width=230)
        #view_image=Button(frame1,text="View image",font=("times new roman",15,"bold"),bd=0,cursor="hand2",bg="gray",command=self.retrieveImages).place(x=600,y=430,width=230)
        submit = Button(frame1, text="Submit", font=("times new roman", 15, "bold"), bd=0,
                        cursor="hand2", bg="Red", command=self.register_data).place(x=370, y=540, width=150)

    # def isValid(self, s):
    #     Pattern = re.compile("[7-9][0-9]{9}")
    #     return Pattern.match(s)

    def register_data(self):
        # valid_no = self.isValid(self.txt_phone_no.get())
        # sqft = self.txt_sq_ft.get()
        # print(sqft)
        # type(sqft)
        # valid_sqft = False
        # if(len(self.txt_phone_no.get()) > 10):
        #     valid_no = False
        # else:
        #     valid_no = False
        if self.cmb_plot_type.get() == "" or self.cmb_plot_type.get() == "Select" or self.txt_name.get() == "" or self.txt_locality.get() == "" or self.txt_price_range.get() == "" or self.txt_sq_ft.get() == "" or self.cmb_type.get() == "" or self.cmb_type.get() == "Select" or self.txt_area.get() == "" or self.txt_phone_no.get() == '':
            messagebox.showerror(
                "Error", "Fill the Required field", parent=self.root)
        # elif(valid_no == False):
        #     messagebox.showerror(
        #         "Error", "Please enter a valid phone number", parent=self.root)
        elif (self.cmb_plot_type.get() == "Building" or self.cmb_plot_type.get() == "Bungalow") and (self.cmb_no_of_rooms.get() == "" or self.cmb_no_of_rooms.get() == "Select"):
            messagebox.showerror(
                "Error", "Number of rooms required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="", database="real_estate")
                cur = conn.cursor()
                if self.cmb_plot_type.get() == "Building":
                    n = (self.txt_area.get())
                    cur.execute(
                        """select area_no from area where area_name=%s""", (n,))
                    result1 = cur.fetchall()
                    for i in result1:
                        r1 = i[0]
                    cur.execute("""select max(Build_id) from Building""")
                    result2 = cur.fetchall()
                    for i in result2:
                        r2 = i[0]
                    cur.execute("insert into Building(Build_id,Build_name,Locality,Rooms,Price_range,Sq_ft,area_no,images,type,owner_detail) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (r2+1, self.txt_name.get(), self.txt_locality.get(), self.cmb_no_of_rooms.get(),
                                 self.txt_price_range.get(), self.txt_sq_ft.get(), r1, self.p, self.cmb_type.get(), self.txt_phone_no.get())
                                )
                elif self.cmb_plot_type.get() == "Bungalow":
                    n = (self.txt_area.get())
                    cur.execute(
                        """select area_no from area where area_name=%s""", (n,))
                    result1 = cur.fetchall()
                    for i in result1:
                        r1 = i[0]
                    cur.execute("""select max(Bung_id) from Bunglow""")
                    result2 = cur.fetchall()
                    for i in result2:
                        r2 = i[0]
                    cur.execute("insert into Bunglow(Bung_id,Bung_name,Locality,Rooms,Price_range,Sq_ft,bung_area_no,images,type,owner_detail) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (r2+1, self.txt_name.get(), self.txt_locality.get(), self.cmb_no_of_rooms.get(),
                                 self.txt_price_range.get(), self.txt_sq_ft.get(), r1, self.p, self.cmb_type.get(), self.txt_phone_no.get())
                                )
                elif self.cmb_plot_type.get() == "Plot":
                    n = (self.txt_area.get())
                    cur.execute(
                        """select area_no from area where area_name=%s""", (n,))
                    result1 = cur.fetchall()
                    for i in result1:
                        r1 = i[0]
                    cur.execute("""select max(P_id) from Plot""")
                    result2 = cur.fetchall()
                    for i in result2:
                        r2 = i[0]
                    cur.execute("insert into Plot(P_id,P_name,Locality,Acres,P_range,Plot_area_no,images,type,owner_detail) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (r2+1, self.txt_name.get(), self.txt_locality.get(), self.txt_sq_ft.get(),
                                 self.txt_price_range.get(), r1, self.p, self.cmb_type.get(), self.txt_phone_no.get())
                                )

                conn.commit()
                conn.close()
                messagebox.showinfo(
                    "Success", "Registration Successful", parent=self.root)
            except Exception as es:
                #messagebox.showerror("Error",f"Error due to :{str(es)}",parent=self.root)
                messagebox.showerror(
                    "Error", "Enter a valid area", parent=self.root)

    # def showimg(self, image_path):
    #     newWindow = Toplevel(root)
    #     newWindow.title("Image")
    #     img = Image.open(image_path)
    #     img.thumbnail((350, 350))
    #     img = ImageTk.PhotoImage(img)
    #     lbl = Label(newWindow, image=img).pack()
    #     newWindow.image = img

    def takeinput(self):
        db = mysql.connector.connect(
            host="localhost", user="root", password="", database="real_estate")
        cur = db.cursor()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select image file", filetypes=(
            ("JPG file", ".jpg"), ("PNG file", ".png"), ("all files", ".")))
        with open(fln, "rb") as file:
            Binarydata = file.read()
        if self.cmb_plot_type.get() == "Building":
            # make path for that particular id
            #cur.execute("""UPDATE building SET images = NULL""")
            if self.j == 1:
                cur.execute("""select max(Build_id) from building""")
                result2 = cur.fetchall()
                for i in result2:
                    r2 = i[0]
                r2 = int(r2)+1
                path = "imageinput/build_imgid"+str(r2)
                os.mkdir(path)
                sqlstmt = """UPDATE building SET images = (%s) WHERE Build_id = %s"""
                cur.execute(sqlstmt, (path, r2, ))
                res1 = db.commit()
                print(res1)
                self.p = path
                self.r = r2
            # take no. of images as input and run a for loop and sore the images as 1.png,2.png.....
            self.storepath = self.p+"/"+str(self.j)+".PNG"
            with open(self.storepath, "wb") as p:
                RES3 = p.write(Binarydata)
                print(RES3)
                p.close()
            #sqlstmt ="""UPDATE building SET images = (%s) WHERE Build_id = %s"""
            #cur.execute(sqlstmt, (self.p,self.r, ))
            #res1 = db.commit()
            # print(res1)
            self.j = self.j+1
        elif self.cmb_plot_type.get() == "Bungalow":
            # make path for that particular id
            if self.j == 1:
                cur.execute("""select max(Bung_id) from Bunglow""")
                result2 = cur.fetchall()
                for i in result2:
                    r2 = i[0]
                r2 = int(r2)+1
                path = "imageinput/bung_imgid"+str(r2)
                os.mkdir(path)
                sqlstmt = """UPDATE Bunglow SET images = (%s) WHERE Bung_id = %s"""
                cur.execute(sqlstmt, (path, r2, ))
                res1 = db.commit()
                print(res1)
                self.p = path
                self.r = r2
            # take no. of images as input and run a for loop and sore the images as 1.png,2.png.....
            self.storepath = self.p+"/"+str(self.j)+".PNG"
            with open(self.storepath, "wb") as p:
                RES3 = p.write(Binarydata)
                print(RES3)
                p.close()
            self.j = self.j+1
        elif self.cmb_plot_type.get() == "Plot":
            # make path for that particular id
            if self.j == 1:
                cur.execute("""select max(P_id) from Plot""")
                result2 = cur.fetchall()
                for i in result2:
                    r2 = i[0]
                r2 = int(r2)+1
                path = "imageinput/plot_imgid"+str(r2)
                os.mkdir(path)
                sqlstmt = """UPDATE Plot SET images = (%s) WHERE P_id = %s"""
                cur.execute(sqlstmt, (path, r2, ))
                res1 = db.commit()
                print(res1)
                self.p = path
                self.r = r2

            # take no. of images as input and run a for loop and sore the images as 1.png,2.png.....
            self.storepath = self.p+"/"+str(self.j)+".PNG"
            with open(self.storepath, "wb") as p:
                RES3 = p.write(Binarydata)
                print(RES3)
                p.close()
            self.j = self.j+1


if(__name__ == "__main__"):
    root.mainloop()
# root = Tk()
# obj = Form(root, 2)
# root.mainloop()

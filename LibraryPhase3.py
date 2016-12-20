import pymysql
from tkinter import *
from re import match
import datetime



class App:


    def __init__(self,master):

        self.master=master
        self.LoginPage()
        self.Register()
        self.register.withdraw()
        import datetime
        now=datetime.datetime.now()
        nowdate=now.date()
        self.nowDate=nowdate
        

    def Connect(self):

        try:
            db=pymysql.connect(host="academic-mysql.cc.gatech.edu",db="cs4400_Group_12",user="cs4400_Group_12",passwd="qubDfpQy")
            return db

        except:
            messagebox.showerror("Unable To Connect","Check Your Internet Connection")
            

    def LoginPage(self):

        self.master.title("Login")

        Label(self.master,text="Username:").grid(row=1,column=0,sticky=E)
        Label(self.master,text="Password:").grid(row=2,column=0,sticky=E)

        self.entry1=Entry(self.master,width=30)
        self.entry1.grid(row=1,column=1)
        self.entry2=Entry(self.master,width=30,show="*")
        self.entry2.grid(row=2,column=1)

        frame=Frame(self.master)
        frame.grid(row=3,column=1,sticky=E)

        Button(frame,text="Login",command=self.LoginCheck).pack(side=RIGHT)
        Button(frame,text="Create Account",command=self.LoginToRegister).pack(side=RIGHT)


    def LoginCheck(self):

        db=self.Connect()
        c=db.cursor()
        self.userName=self.entry1.get()
        password=self.entry2.get()

        SQL1="SELECT UserName,Password FROM USER WHERE UserName=%s AND Password=%s"
        SQL2="SELECT UserName FROM STAFF WHERE UserName=%s"

        affected1=c.execute(SQL1,(self.userName,password))
        affected2=c.execute(SQL2,(self.userName))
        
        
        if affected1==1 or affected2==1:
 
            messagebox.showinfo("Success","Logged in successfully")
            if affected1==1:
                self.master.withdraw()
                self.menu1()
            elif affected2 ==1:
                self.master.withdraw()
                self.menu2()
            
        else:
            messagebox.showerror("Error","The username/password combination is unrecognizable")           
            return None

    def LoginToRegister(self):

        self.register.deiconify()
        self.master.withdraw()
 

    def Register(self):

        self.register=Toplevel()
        self.register.title("New User Registration")
        
        Label(self.register,text="Username:").grid(row=2,column=0,sticky=W)
        Label(self.register,text="Password:").grid(row=3,column=0,sticky=W)
        Label(self.register,text="Confirm Password:").grid(row=4,column=0,sticky=W)
        
        self.entry3=Entry(self.register,width=30)
        self.entry3.grid(row=2,column=1)
        self.entry4=Entry(self.register,width=30,show="*")
        self.entry4.grid(row=3,column=1)
        self.entry5=Entry(self.register,width=30,show="*")
        self.entry5.grid(row=4,column=1)

        Button(self.register,text="Register",command=self.RegisterDB).grid(row=5,column=2)
        Button(self.register,text="Back",command=self.ttttt).grid(row=5,column=3)

    def ttttt(self):
        self.register.withdraw()
        self.master.deiconify()


    def RegisterDB(self):

        userName=self.entry3.get()
        password1=self.entry4.get()
        password2=self.entry5.get()

        if userName=="":

            messagebox.showerror("Error!","Enter the Username")
            return None

        if password1=="":

            messagebox.showerror("Error!","Enter the Password")
            return None

        if password1!=password2:

            messagebox.showerror("Error!","Password entrered do not match")
            return None

        db=self.Connect()
        c=db.cursor()

        SQL="SELECT * FROM USER WHERE Username=%s"
        affected=c.execute(SQL,userName)

        if affected!=0:

            messagebox.showerror("Error!","Username has already been used")
            self.entry3.delete(0,last=END)
            self.entry4.delete(0,last=END)
            self.entry5.delete(0,last=END)
            return None

        c.execute("INSERT INTO USER (Username,Password) VALUES (%s,%s)",(userName,password1))

        messagebox.showinfo("Success", "Registration is complete")
        
        
        db.commit()
        c.close()
        db.close()

        self.RegisterToCreateProfile()
        

    def CreateProfile(self):

        self.profile=Toplevel()
        self.profile.title("Create Profile")

            
        Label(self.profile,text="First Name").grid(row=0,column=0,sticky=W)
        Label(self.profile,text="D.O.B").grid(row=1,column=0,sticky=W)
        Label(self.profile,text="Email").grid(row=2,column=0,sticky=W)
        Label(self.profile,text="Address").grid(row=3,column=0,sticky=W)
        Label(self.profile,text="   Last Name").grid(row=0,column=2,sticky=W)
        Label(self.profile,text="   Gender").grid(row=1,column=2,sticky=W)
        Label(self.profile,text="   Are you a faculty member?").grid(row=2,column=2,sticky=W)
        Label(self.profile,text="   ").grid(row=4,column=2,sticky=W)

        self.entry6=Entry(self.profile,width=20)
        self.entry6.grid(row=0,column=1)
        self.entry7=Entry(self.profile,width=10)
        self.entry7.grid(row=1,column=1,sticky=W)
        self.entry7.insert(0,"YYYY-MM-DD")
        self.entry7.bind("<Button-1>", lambda event:self.entry7.delete(0,END))
        self.entry8=Entry(self.profile,width=20)
        self.entry8.grid(row=2,column=1)
        self.entry9=Entry(self.profile,width=20)
        self.entry9.grid(row=3,column=1,rowspan=2,sticky=N+S)
        self.entry10=Entry(self.profile,width=20)
        self.entry10.grid(row=0,column=3,sticky=W+E)

        self.spinbox1=Spinbox(self.profile,values=("Select Gender","Male","Female"))
        self.spinbox1.grid(row=1,column=3)

        self.iv = IntVar()

        self.checkbutton1=Checkbutton(self.profile, text="Yes", variable=self.iv,command=lambda ind=self.iv.get():self.showDeptList(ind))
        self.checkbutton1.grid(row=2,column=3)

        Button(self.profile,text="Submit",command=self.CreateProfileDB).grid(row=5,column=3)


    def CreateProfileDB(self):

        fName=self.entry6.get()
        lName=self.entry10.get()
        email=self.entry8.get()
        address=self.entry9.get()
        dob=self.entry7.get()
        gender=self.spinbox1.get()
        userName=self.entry3.get()

        try:
            department=self.spinbox2.get()

        except AttributeError:
            department=None
        
        db=self.Connect()
        c=db.cursor()

        SQL="INSERT INTO STUDENT_FACULTY(First_Name, Last_Name, D_O_B, Email, Address, Gender, Dept, UserName) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        c.execute(SQL,(fName,lName,dob, email, address, gender,department,userName))

        db.commit()
        c.close()
        db.close()

        self.menu1()
        self.profile.withdraw()


    def menu1(self):

        
        self.menu1=Toplevel()
        self.menu1.title("HomePage")

        Label(self.menu1,text="What would you like to do?").grid(row=0,column=0,sticky=EW)
        self.iiv = IntVar()
        
        Radiobutton(self.menu1, text="Search books", variable=self.iiv, value=1).grid(row=1,column=0,sticky=W)
        Radiobutton(self.menu1, text="Request extension", variable=self.iiv,value=2).grid(row=2,column=0,sticky=W)
        Radiobutton(self.menu1, text="Track Location", variable=self.iiv,value=3).grid(row=3,column=0,sticky=W)
        Radiobutton(self.menu1, text="Check out", variable=self.iiv,value=4).grid(row=4,column=0,sticky=W)
        Button(self.menu1,text="Submit",command=self.goTo1).grid(row=5, column=0, sticky=EW)

    def menu2(self):
        self.menu2=Toplevel()
        self.menu2.title("HomePage")

        Label(self.menu2,text="What would you like to do?").grid(row=0,column=0,sticky=EW)
        self.iiv2 = IntVar()
        
        Radiobutton(self.menu2, text="Return Book", variable=self.iiv2, value=1).grid(row=1,column=0,sticky=W)
        Radiobutton(self.menu2, text="Lost/Damage Penalty", variable=self.iiv2,value=2).grid(row=2,column=0,sticky=W)
        Radiobutton(self.menu2, text="Damaged Report", variable=self.iiv2,value=3).grid(row=3,column=0,sticky=W)
        Radiobutton(self.menu2, text="Popular Books Report", variable=self.iiv2,value=4).grid(row=4,column=0,sticky=W)
        Radiobutton(self.menu2, text="Frequent User Report", variable=self.iiv2,value=5).grid(row=5,column=0,sticky=W)
        Radiobutton(self.menu2, text="Popular Subject Report", variable=self.iiv2,value=6).grid(row=6,column=0,sticky=W)
        Button(self.menu2,text="Submit",command=self.goTo2).grid(row=7, column=0, sticky=EW)
        

    def goTo1(self):
        self.menu1.withdraw()
        self.choice=self.iiv.get()
        if self.choice==1:
            self.searchBook()
        elif self.choice==2:
            self.extensionF()
        elif self.choice==3:
            self.trackLocation()
        elif self.choice==4:
            self.bookCheckout()
        else:
            messagebox.showinfo("Sorry", "Please choose one")

    def goTo2(self):
        self.menu2.withdraw()
        self.choice2=self.iiv2.get()
        if self.choice2==1:
            self.returnBook()
        elif self.choice2==2:
            self.penalty()
        elif self.choice2==3:
            self.damagedReport()
        elif self.choice2==4:
            self.popBooksReport()
        elif self.choice2==5:
            self.frequentUserReport()
        elif self.choice2==6:
            self.popSubjectReport() 
        else:
            messagebox.showinfo("Sorry", "Please choose one")
                

    def showDeptList(self,ind):    

        if self.iv.get()==1:
            self.label=Label(self.profile,text="   Associated Department")
            self.label.grid(row=3,column=2,sticky=W)
            self.spinbox2=Spinbox(self.profile,values=("Select Department"))
            self.spinbox2.grid(row=3,column=3)

        else:

            self.label.grid_remove()
            self.spinbox2.grid_remove()


    def RegisterToCreateProfile(self):

        self.register.withdraw()
        self.CreateProfile()

        
    def searchBook(self):

        self.searchbook=Toplevel()
        self.searchbook.title("Search Books")

        Label(self.searchbook,text="ISBN").grid(row=0,column=0)
        Label(self.searchbook,text="Title").grid(row=1,column=0)
        Label(self.searchbook,text="Author").grid(row=2,column=0)
        Label(self.searchbook,text="").grid(row=3,column=0)

        self.entry11=Entry(self.searchbook,width=20)
        self.entry11.grid(row=0,column=1)
        self.entry12=Entry(self.searchbook,width=20)
        self.entry12.grid(row=1,column=1)
        self.entry13=Entry(self.searchbook,width=20)
        self.entry13.grid(row=2,column=1)

        Button(self.searchbook,text="Back",command=self.trans3).grid(row=4,column=0)
        Button(self.searchbook,text="Search",command=self.searchBookDB).grid(row=4,column=1)
        
    def trans3(self):
        self.searchbook.withdraw()
        self.menu1.deiconify()

    def searchBookDB(self):
        
        db=self.Connect()
        c=db.cursor()
        import datetime
        now=datetime.datetime.now()
        nowdate=now.date()
        self.nowDate=nowdate
        if self.entry11.get()!="" and self.entry12.get()=="" and self.entry13.get()=="":
            SQL="""SELECT R.ISBN, R.Copy_Number, R.Return_Date, B.Is_On_Reserve, C.Is_On_Hold FROM BOOK AS B NATURAL JOIN BOOK_COPY AS C NATURAL JOIN ISSUES_RECORD AS R WHERE B.ISBN=%s """            
            c.execute(SQL,self.entry11.get())
            result=c.fetchall()
            
            if result == ():
                SQL1="""SELECT Is_On_Reserve FROM BOOK WHERE ISBN=%s"""
                c.execute(SQL1,self.entry11.get())
                b=c.fetchall()
                if b==():
                    messagebox.showinfo("Info","0 Matches")
                    return None
                elif b[0]==(1,):
                    messagebox.showinfo("Sorry", "This book is on reserved therefore not available for checkout")
                    return None
                else:
                    SQL1="SELECT ISBN, Copy_Number, Is_On_Hold FROM BOOK_COPY WHERE ISBN = %s"
                    c1=db.cursor()
                    c1.execute(SQL1,self.entry11.get())
                    All=c1.fetchall()
                    self.ava=[]
                    for item in All:
                        new=(item[0],item[1],nowdate,item[2])
                        self.ava.append(new)
                    self.ava.sort()

            else:
                self.ava=[]
                dic={}
                a=list(result)                
                a.sort()
                for item in a:
                    dic[(item[0],item[1])]=(item[2],item[-1])
                
                keys=dic.keys()
                
                SQL2="SELECT ISBN, Copy_Number, Is_On_Hold FROM BOOK_COPY WHERE ISBN = %s"
                c2=db.cursor()
                c2.execute(SQL2,self.entry11.get())
                All=c2.fetchall()
                

                for item in All:
                    if (item[0],item[1]) not in keys:
                        dic[item[0],item[1]]=(nowdate,item[-1])
                    
                for key in dic.keys():
                    new=(key[0],key[1],dic[key][0],dic[key][1])
                    self.ava.append(new)
                
                self.ava.sort()
            self.holdfun()
                
        elif self.entry12.get() != "" and self.entry11.get()=="" and self.entry13.get()=="":
            
            
            SQL1="SELECT B.ISBN, B.Is_On_Reserve FROM BOOK AS B WHERE B.Title LIKE %s"
            c1=db.cursor()
            c1.execute(SQL1,("%"+self.entry12.get()+"%"))
            bookList=list(c1.fetchall())

            avaBook=[]
            self.resBook=[]

            for book in bookList:
                if book[1]==1:
                    self.resBook.append(book[0])
                else:
                    avaBook.append(book[0])

            self.ava1=[]
            for isbn in avaBook:
                
                cc=db.cursor()
                
                SQL="""SELECT R.ISBN, R.Copy_Number, R.Return_Date, B.Is_On_Reserve, C.Is_On_Hold FROM BOOK AS B NATURAL JOIN BOOK_COPY AS C NATURAL JOIN ISSUES_RECORD AS R WHERE B.ISBN=%s """            
                cc.execute(SQL,isbn)
                result=cc.fetchall()
                
                if result == ():
                    c=db.cursor()
                    SQL1="""SELECT Is_On_Reserve FROM BOOK WHERE ISBN=%s"""
                    c.execute(SQL1,isbn)
                    b=c.fetchall()
                    if b==():
                        messagebox.showinfo("Info","0 Matches")
                        return None
                    else:
                        SQL1="SELECT ISBN, Copy_Number, Is_On_Hold FROM BOOK_COPY WHERE ISBN = %s"
                        c1=db.cursor()
                        c1.execute(SQL1,isbn)
                        All=c1.fetchall()
                        self.small=[]
                        for item in All:
                            new=(item[0],item[1],nowdate,item[2])
                            self.small.append(new)
                        self.small.sort()
                        self.ava1.append(self.small)

                else:
                    self.small=[]
                    dic={}
                    a=list(result)                
                    a.sort()
                    for item in a:
                        dic[(item[0],item[1])]=(item[2],item[-1])
                    
                    keys=dic.keys()
                    
                    SQL2="SELECT ISBN, Copy_Number, Is_On_Hold FROM BOOK_COPY WHERE ISBN = %s"
                    ccc=db.cursor()
                    ccc.execute(SQL2,isbn)
                    All=ccc.fetchall()
                    

                    for item in All:
                        if (item[0],item[1]) not in keys:
                            dic[item[0],item[1]]=(nowdate,item[-1])
                        
                    for key in dic.keys():
                        new=(key[0],key[1],dic[key][0],dic[key][1])
                        self.small.append(new)
                    
                    self.small.sort()
                    self.ava1.append(self.small)
                    
            self.ava=[]
            for book in self.ava1:
                for copy in book:
                    self.ava.append(copy)
            self.holdfun()               
            

        elif self.entry13.get() != "" and self.entry11.get()=="" and self.entry12.get()=="":

            SQL1="SELECT B.ISBN, B.Is_On_Reserve,A.Author_Name FROM BOOK AS B NATURAL JOIN AUTHOR AS A WHERE A.Author_Name LIKE %s"
            c1=db.cursor()
            c1.execute(SQL1,("%"+self.entry13.get()+"%"))
            bookList=list(c1.fetchall())

            avaBook=[]
            self.resBook=[]

            for book in bookList:
                if book[1]==1:
                    self.resBook.append(book[0])
                else:
                    avaBook.append(book[0])

            self.ava1=[]
            for isbn in avaBook:
                
                cc=db.cursor()
                
                SQL="""SELECT R.ISBN, R.Copy_Number, R.Return_Date, B.Is_On_Reserve, C.Is_On_Hold FROM BOOK AS B NATURAL JOIN BOOK_COPY AS C NATURAL JOIN ISSUES_RECORD AS R WHERE B.ISBN=%s """            
                cc.execute(SQL,isbn)
                result=cc.fetchall()
                
                if result == ():
                    c=db.cursor()
                    SQL1="""SELECT Is_On_Reserve FROM BOOK WHERE ISBN=%s"""
                    c.execute(SQL1,isbn)
                    b=c.fetchall()
                    if b==():
                        messagebox.showinfo("Info","0 Matches")
                        return None
                    else:
                        SQL1="SELECT ISBN, Copy_Number, Is_On_Hold FROM BOOK_COPY WHERE ISBN = %s"
                        c1=db.cursor()
                        c1.execute(SQL1,isbn)
                        All=c1.fetchall()
                        self.small=[]
                        for item in All:
                            new=(item[0],item[1],nowdate,item[2])
                            self.small.append(new)
                        self.small.sort()
                        self.ava1.append(self.small)

                else:
                    self.small=[]
                    dic={}
                    a=list(result)                
                    a.sort()
                    for item in a:
                        dic[(item[0],item[1])]=(item[2],item[-1])
                    
                    keys=dic.keys()
                    
                    SQL2="SELECT ISBN, Copy_Number, Is_On_Hold FROM BOOK_COPY WHERE ISBN = %s"
                    ccc=db.cursor()
                    ccc.execute(SQL2,isbn)
                    All=ccc.fetchall()
                    

                    for item in All:
                        if (item[0],item[1]) not in keys:
                            dic[item[0],item[1]]=(nowdate,item[-1])
                        
                    for key in dic.keys():
                        new=(key[0],key[1],dic[key][0],dic[key][1])
                        self.small.append(new)
                    
                    self.small.sort()
                    self.ava1.append(self.small)
                    
            self.ava=[]
            for book in self.ava1:
                for copy in book:
                    self.ava.append(copy)
            self.holdfun()
       
        
        else:

            messagebox.showerror("Error","Input only in one of the category")

        db.commit()
        db.close()
        c.close()
            
        
        
    def extensionF(self):
        self.extension=Toplevel()
        self.extension.title("Request extension")
        Label(self.extension,text="Book(s) checked out by you").grid(row=0,column=0,sticky=EW)
        Button(self.extension,text="Search records",command=self.extensionDB).grid(row=1,column=0)
        
    def extensionDB(self):
        db=self.Connect()
        c=db.cursor()
        SQL="""SELECT R.Date_Of_issue, R.Return_Date, R.Count_of_extensions, R.ISBN,R.Copy_Number, C.Is_On_Hold, R.Issue_ID, R.Extension_Date FROM BOOK_COPY AS C, ISSUES_RECORD AS R WHERE C.ISBN=R.ISBN AND C.Copy_Number = R.Copy_Number AND R.Username=%s"""
        c.execute(SQL,self.userName)
        self.issueData=c.fetchall()
        self.rowNumber=2

        SQL1="SELECT Is_Faculty FROM STUDENT_FACULTY WHERE UserName=%s"
        c1=db.cursor()
        c1.execute(SQL1,self.userName)
        usertype=c1.fetchall()

        yes=0

        if len(self.issueData)==0:
            messagebox.showerror("Error","You have not borrowed any books yet")
            self.extension.withdraw()
            self.menu1.deiconify()
            yes=yes+1
                   
        for item in self.issueData:
            if item[2]== None:
                self.times=0
            else:
                self.times=item[2]
                
            oneRow="|Issue ID: "+str(item[-2])+ "|Book ISBN: "+str(item[3])+" |Copy Number: "+str(item[4])+" |Issue Date: "+str(item[0])+"|Expected return date: "+str(item[1])+" |You've requsted extension(s) "+str(self.times)+ " times|"
            Label(self.extension,text=oneRow).grid(row=self.rowNumber,column=0,sticky=EW)
            self.rowNumber =self.rowNumber+1

        self.buttonRow=2    
        self.iivv = IntVar()


        buttoncount=0
        for item in self.issueData:
            
            dateDif=item[1]-item[0]
            checkoutDays=dateDif.days
            
            if item[2]== None:
                self.time=0
            else:
                self.time=item[2]
            now = datetime.datetime.now()
            nowdate=now.date()


            if self.time < 2 and usertype[0][0]==0 and item[-3]==0 and checkoutDays<27 and (nowdate < item[1]):
                Radiobutton(self.extension,text=" ",variable=self.iivv,value=int(self.buttonRow-2)).grid(row=self.buttonRow,column=1)
                buttoncount=buttoncount+1

            elif self.time < 5 and usertype[0][0]==1 and item[-3]==0 and checkoutDays<55 and (nowdate < item[1]):
                Radiobutton(self.extension,text="Request extension",variable=self.iivv,value=int(self.buttonRow-2)).grid(row=self.buttonRow,column=1)
                buttoncount=buttoncount+1

            elif item[-3]==1:
                Label(self.extension,text="|The Book is on future hold|").grid(row=self.buttonRow,column=1)
                
            else:
                Label(self.extension,text="|No more extension allowed|").grid(row=self.buttonRow,column=1)

            self.buttonRow =self.buttonRow+1
        
        
        
        Button(self.extension,text="Request",command=self.requestExtension).grid(row=self.buttonRow+1,column=2)
        
        if buttoncount== 0 and yes!=1:
            messagebox.showerror("Error","You cannot request extension")
            self.extension.withdraw()
            self.menu1.deiconify()

        db.commit()
        db.close()
        c.close()

            
        

    def requestExtension(self):
            self.extension.withdraw()
        
            Rqst=self.issueData[self.iivv.get()]

            if Rqst[2]== None:
                    self.counts=0
            else:
                    self.counts=Rqst[2]
                    
            import datetime

            
            now = datetime.datetime.now()

            returnDate=Rqst[1]+datetime.timedelta(days=14)
            
            dateDif=now.date()-Rqst[0]
            checkoutDays=dateDif.days

            if checkoutDays <14:
                returnDate=now.date()+datetime.timedelta(days=13)
            else:
                returnDate=Rqst[0]+datetime.timedelta(days=27)


            self.ext2win=Toplevel()
            self.ext2win.title("Confirm extension")

            Label(self.ext2win,text="Original Checkout Date: ").grid(row=0,column=0,sticky=W)
            Label(self.ext2win,text="Current extension Date: ").grid(row=1,column=0,sticky=W)
            Label(self.ext2win,text="Curent return Date: ").grid(row=1,column=2,sticky=W)
            Label(self.ext2win,text="New extension Date: ").grid(row=2,column=0,sticky=W)
            Label(self.ext2win,text="New estimated return Date: ").grid(row=2,column=2,sticky=W)

            self.svv1=StringVar()
            self.svv2=StringVar()
            self.svv3=StringVar()
            self.svv4=StringVar()
            self.svv5=StringVar()
            
            self.entryy1=Entry(self.ext2win,textvariable=self.svv1,width=20).grid(row=0,column=1)
            self.entryy2=Entry(self.ext2win,textvariable=self.svv2,width=20).grid(row=1,column=1)
            self.entryy3=Entry(self.ext2win,textvariable=self.svv3,width=20).grid(row=1,column=3)
            self.entryy4=Entry(self.ext2win,textvariable=self.svv4,width=20).grid(row=2,column=1)
            self.entryy5=Entry(self.ext2win,textvariable=self.svv5,width=20).grid(row=2,column=3)

            self.svv1.set(str(Rqst[0]))
            self.svv2.set(str(Rqst[-1]))
            self.svv3.set(str(Rqst[1]))
            self.svv4.set(str(now.date()))
            self.svv5.set(str(returnDate))

            Button(self.ext2win,text="Submit",command=self.ext2).grid(row=3,column=3)

            self.tup=(now.date(),int(self.counts+1),returnDate,Rqst[-2])

    def ext2(self):

        db=self.Connect()

        SQL="SELECT Is_Debarred FROM STUDENT_FACULTY WHERE UserName=%s"
        ccc=db.cursor()
        ccc.execute(SQL,self.userName)
        de=ccc.fetchall()
        deb=de[0][0]
        if deb == 1:
            messagebox.showerror("Error","This user is debarred")
            self.ext2win.withdraw()
            self.menu1.deiconify()
        else:
        
            c2 = db.cursor()
            SQL="UPDATE ISSUES_RECORD SET Extension_Date=%s, Count_of_extensions=%s,Return_Date=%s WHERE Issue_ID=%s"
            c2.execute(SQL,self.tup)
            messagebox.showinfo("Success","You've successfully extended the return date")

        db.commit()
        db.close()
        
    def trackLocation(self):
        
        self.track=Toplevel()
        self.track.title("Track Book Location")

        
        frame1=Frame(self.track)
        frame1.pack()
        frame2=Frame(self.track)
        frame2.pack()

        self.sv1=StringVar()
        self.sv2=StringVar()
        self.sv3=StringVar()
        self.sv4=StringVar()
        
        Label(frame1,text="ISBN").grid(row=0,column=0)
        Label(frame2,text="Floor Number").grid(row=0,column=0)
        Label(frame2,text="Aisle Number").grid(row=1,column=0)
        Label(frame2,text="Shelf Number").grid(row=0,column=2)
        Label(frame2,text="Subject").grid(row=1,column=2)
        
        self.entryt1=Entry(frame1,width=20)
        self.entryt1.grid(row=0,column=1)
        Entry(frame2,width=10,textvariable=self.sv1,state="readonly").grid(row=0,column=1)
        Entry(frame2,width=10,textvariable=self.sv2,state="readonly").grid(row=1,column=1)
        Entry(frame2,width=10,textvariable=self.sv3,state="readonly").grid(row=0,column=3)
        Entry(frame2,width=10,textvariable=self.sv4,state="readonly").grid(row=1,column=3)
        
        Button(frame1,text="Locate",command=self.trackLocationDB).grid(row=0,column=2)
        Button(frame1,text="Back",command=self.transs).grid(row=2,column=3)

    def transs(self):
        self.track.withdraw()
        self.menu1.deiconify()

        
    def trackLocationDB(self):

        db=self.Connect()
        c=db.cursor()

        SQL="SELECT S.Floor_Number,Z.Shelf_Number,S.Aisle_Number,Z.Subject_Name FROM BOOK AS Z,SHELF AS S WHERE Z.Shelf_Number=S.Shelf_Number AND Z.ISBN=%s"
        c.execute(SQL,self.entryt1.get())
        data=c.fetchall()

        self.sv1.set(data[0][0])
        self.sv2.set(data[0][2])
        self.sv3.set(data[0][1])
        self.sv4.set(data[0][3])

        

        db.commit()
        c.close()
        db.close()

    def holdfun(self):
        db=self.Connect()
       
        self.searchbook.withdraw()
        self.hold=Toplevel()
        self.hold.title("Request Hold")

        Label(self.hold,text="Instant Hold").grid(row=0,column=0)
        Label(self.hold,text="Future Hold").grid(row=0,column=1)
        Label(self.hold,text="ISBN").grid(row=0,column=2)
        Label(self.hold,text="Title").grid(row=0,column=3)
        Label(self.hold,text="Edition").grid(row=0,column=4)
        Label(self.hold,text="Copy number").grid(row=0,column=5)
        Label(self.hold,text="Earliest Available Date").grid(row=0,column=6)

        rownum=1
        self.iivy = IntVar()
        
        for record in self.ava:
            SQL = 'SELECT Title,Edition FROM BOOK WHERE ISBN=%s' 
            c=db.cursor()
            c.execute(SQL,record[0])
            resul = c.fetchall()
            result = resul[0]
            name = result[0]
            edi = result[1]
           
            Label(self.hold,text=record[0]).grid(row=rownum,column=2)
            Label(self.hold,text=name).grid(row=rownum,column=3)
            Label(self.hold,text=edi).grid(row=rownum,column=4)
            Label(self.hold,text=record[1]).grid(row=rownum,column=5)
            Label(self.hold,text=record[2]).grid(row=rownum,column=6)
            if record[2] <= self.nowDate:
                Radiobutton(self.hold, text=" ", variable=self.iivy, value=rownum).grid(row=rownum,column=0,sticky=EW)
            else:
                Radiobutton(self.hold, text=" ", variable=self.iivy, value=rownum).grid(row=rownum,column=1,sticky=EW)
            rownum=rownum+1
            
        Label(self.hold,text='Hold Request Date').grid(row=rownum,column=0)
        Label(self.hold,text=self.nowDate).grid(row=rownum,column=1)
        Label(self.hold,text='Estimated Return Date').grid(row=rownum,column=2)
        Label(self.hold,text=self.nowDate+datetime.timedelta(days=17)).grid(row=rownum,column=3)
        Button(self.hold,text='Back',command=self.trans).grid(row=rownum+1,column=1)
        Button(self.hold,text='Submit',command=self.holdDB).grid(row=rownum+1,column=2)
        Button(self.hold,text='Cancel',command=self.trans2).grid(row=rownum+1,column=3)

        try:
            if len(self.resBook) > 0:

                Label(self.hold,text='Reserved Book:    ').grid(row=rownum+2,column=0)
                n=rownum+3

                

                for isbn in self.resBook:
                    SQL = 'SELECT Title,Edition FROM BOOK WHERE ISBN=%s' 
                    c=db.cursor()
                    c.execute(SQL,isbn)
                    resul = c.fetchall()
                    result = resul[0]
                    name = result[0]
                    edi = result[1]
                    info="ISBN: "+str(isbn)+"|  Title: "+str(name)+"|  Edition: "+str(edi)
                    Label(self.hold,text=info).grid(row=n,column=0,columnspan=3)
                    n=n+1
        except:
            pass

        db.commit()
        db.close()
    

           

    def trans(self):
        self.hold.withdraw()
        self.searchbook.deiconify()
    def trans2(self):
        self.hold.withdraw()
        self.menu1.deiconify()

        
    def holdDB(self):
        db=self.Connect()

        SQL="SELECT Is_Debarred FROM STUDENT_FACULTY WHERE UserName=%s"
        ccc=db.cursor()
        ccc.execute(SQL,self.userName)
        de=ccc.fetchall()
        deb=de[0][0]
        if deb == 1:
            messagebox.showerror("Error","This user is debarred")
            self.hold.withdraw()
            self.menu1.deiconify()

        else:
        
            c=db.cursor()
            c1=db.cursor()
            book = self.ava[self.iivy.get()-1]
            hold_req_date = self.nowDate
            if book[2] > hold_req_date:

                hold_req_date = book[2]
            SQL = 'INSERT INTO ISSUES_RECORD(Date_of_issue,Return_Date,UserName,ISBN,Copy_Number,Hold_Request_Date) VALUES (%s,%s,%s,%s,%s,%s)'
            c.execute(SQL,(hold_req_date+datetime.timedelta(days=3),hold_req_date+datetime.timedelta(days=17),self.userName,book[0],book[1],hold_req_date))

            SQL1="UPDATE BOOK_COPY SET Is_Checked_Out=0, Is_On_Hold=1,Future_Requester=%s WHERE Copy_Number=%s AND ISBN=%s"
            c1.execute(SQL1,(self.userName,book[1],book[0]))

            db.commit()

            cur=db.cursor()

            SQL3 = "SELECT Issue_ID FROM ISSUES_RECORD WHERE Date_of_issue=%s AND Return_Date=%s AND UserName=%s AND ISBN=%s AND Copy_Number=%s AND Hold_Request_Date=%s"
            cur.execute(SQL3,(hold_req_date+datetime.timedelta(days=3),hold_req_date+datetime.timedelta(days=17),self.userName,book[0],book[1],hold_req_date))
            isI=cur.fetchall()
            isID=isI[0][0]

            messagebox.showinfo("Success", "You've placed a hold on this book."+"Please write down your issue record for furture checkout: "+str(isID))
            self.hold.withdraw()
            self.menu1.deiconify()

            c.close()
            c1.close()

        
        db.close()

    

    def bookCheckout(self):

        self.checkout=Toplevel()
        self.checkout.title("Book Checkout")

        frame1=Frame(self.checkout)
        frame1.pack()
        frame2=Frame(self.checkout)
        frame2.pack()

        self.svb1=StringVar()
        self.svb2=StringVar()
        self.svb3=StringVar()
        self.svb4=StringVar()
        self.svb5=StringVar()

        Label(frame1,text="Issue Id").grid(row=0,column=0)
        Label(frame1,text="ISBN").grid(row=1,column=0)
        Label(frame1,text="Check out Date").grid(row=2,column=0)
        Label(frame1,text="User Name").grid(row=0,column=2)
        Label(frame1,text="Copy #").grid(row=1,column=2)
        Label(frame1,text="Estimated Return Date").grid(row=2,column=2)

        self.entryb1=Entry(frame1)
        self.entryb1.grid(row=0,column=1)
        Entry(frame1,textvariable=self.svb1,state="readonly").grid(row=1,column=1)
        Entry(frame1,textvariable=self.svb2,state="readonly").grid(row=2,column=1)
        Entry(frame1,textvariable=self.svb3,state="readonly").grid(row=0,column=3)
        Entry(frame1,textvariable=self.svb4,state="readonly").grid(row=1,column=3)
        Entry(frame1,textvariable=self.svb5,state="readonly").grid(row=2,column=3)

        Button(frame2,text="Confirm",command=self.bookCheckoutDB).pack()
        Button(frame2,text="Back",command=self.trans4).pack()

    def trans4(self):
        self.checkout.withdraw()
        self.menu1.deiconify()

    def bookCheckoutDB(self):

        db=self.Connect()
        c = db.cursor()
        c1 = db.cursor()
        c2 = db.cursor()

        SQL="SELECT Is_Debarred FROM STUDENT_FACULTY WHERE UserName=%s"
        ccc=db.cursor()
        ccc.execute(SQL,self.userName)
        de=ccc.fetchall()
        deb=de[0][0]
        if deb == 1:
            messagebox.showerror("Error","This user is debarred")
            self.checkout.withdraw()
            self.menu1.deiconify()

        else:
            

            SQL="SELECT UserName,ISBN,Copy_Number,Date_of_issue,Return_Date,Hold_Request_Date FROM ISSUES_RECORD WHERE Issue_ID = %s"
            c.execute(SQL,self.entryb1.get())
            dat=c.fetchall()
            data=dat[0]
            try:

                if data[0]==self.userName:
                

                    if self.nowDate <= data[-1]+datetime.timedelta(days=3):
                        self.svb1.set(data[1])
                        self.svb2.set(self.nowDate)
                        self.svb3.set(data[0])
                        self.svb4.set(data[2])
                        self.svb5.set(self.nowDate+datetime.timedelta(days=14))

                        SQL1="UPDATE ISSUES_RECORD SET Date_of_issue=%s, Return_Date=%s WHERE Issue_ID=%s"
                        c2.execute(SQL1,(self.nowDate,self.nowDate+datetime.timedelta(days=14),self.entryb1.get()))
                        
                        SQL2="UPDATE BOOK_COPY SET Is_Checked_Out=1, Is_On_Hold=0, Future_Requester=%s WHERE Copy_Number=%s AND ISBN=%s"
                        c1.execute(SQL2,("",data[2],data[1]))
             
                        messagebox.showinfo("Success","You've checked out the book.")

                        
                    else:
                        SQL="DELETE FROM ISSUES_RECORD WHERE Issue_ID=%s"
                        c1.execute(SQL,self.entryb1.get())
                        messagebox.showerror("Sorry","This hold has been droped, try another one.")
                else:
                    a=1+"1"
            except:
                messagebox.showerror("Sorry","This Issue-ID is not your valid hold request,try again.")
   
            
        db.commit()
        db.close()
        

    def returnBook(self):

        self.bookreturn=Toplevel()
        self.bookreturn.title("Return Book")

        Label(self.bookreturn,text="Issue Id").grid(row=0,column=0)
        Label(self.bookreturn,text="ISBN").grid(row=1,column=0)
        Label(self.bookreturn,text="Return in Damaged Condition").grid(row=2,column=0)
        Label(self.bookreturn,text="Copy Number").grid(row=1,column=2)
        Label(self.bookreturn,text="User Name").grid(row=2,column=2)

        self.svr1=StringVar()
        self.svr2=StringVar()
        self.svr3=StringVar()
        self.svr4=StringVar()

        self.entryr1=Entry(self.bookreturn)
        self.entryr1.grid(row=0,column=1)
        Entry(self.bookreturn,textvariable=self.svr1,state="readonly").grid(row=1,column=1)
        Entry(self.bookreturn,textvariable=self.svr3,state="readonly").grid(row=1,column=3)
        Entry(self.bookreturn,textvariable=self.svr4,state="readonly").grid(row=2,column=3)

        self.svr2.set("Select")
        OptionMenu(self.bookreturn, self.svr2,"Yes","No").grid(row=2,column=1)

        Button(self.bookreturn,text="Verify Id",command=self.returnBookDB1).grid(row=3,column=2,sticky=E)
        Button(self.bookreturn,text="Return Book",command=self.returnBookDB2).grid(row=3,column=3,sticky=E)
        Button(self.bookreturn,text="Back",command=self.tr).grid(row=3,column=4,sticky=E)
    def tr(self):
        self.bookreturn.withdraw()
        self.menu2.deiconify()


    def returnBookDB1(self):

        db=self.Connect()
        c=db.cursor()

        SQL1="SELECT ISBN,Copy_Number,UserName FROM ISSUES_RECORD WHERE Issue_ID=%s"
        c.execute(SQL1,self.entryr1.get())
        self.data=c.fetchall()

        try:
            self.svr1.set(self.data[0][0])
            self.svr3.set(self.data[0][1])
            self.svr4.set(self.data[0][2])

        except IndexError:
            messagebox.showerror("Sorry","Invalid Issue-ID")

        db.commit()
        c.close()
        db.close()
        

    def returnBookDB2(self):

        db=self.Connect()
        c=db.cursor()
        
        SQL2="UPDATE BOOK_COPY SET Is_Checked_Out=%s WHERE ISBN=%s AND Copy_Number=%s"
        c.execute(SQL2,(0,self.data[0][0],self.data[0][1]))
        messagebox.showinfo("Success","Book returned")
        

        if self.svr2.get()=="Yes":

            SQL3="UPDATE BOOK_COPY SET Is_Damaged=%s WHERE ISBN=%s AND Copy_Number=%s"
            c.execute(SQL3,(1,self.data[0][0],self.data[0][1]))
            messagebox.showinfo("Notice","Charged for damage")

        SQL4="SELECT Return_Date FROM ISSUES_RECORD WHERE Issue_ID=%s"
        c.execute(SQL4,self.entryr1.get())
        data=c.fetchall()
        returnDate=data[0][0]

        if self.nowDate>returnDate:

            SQL5="SELECT Penalty FROM STUDENT_FACULTY WHERE UserName=%s"

            SQL6="UPDATE STUDENT_FACULTY SET Penalty=%s WHERE Username=%s"
        
            c.execute(SQL5,self.data[0][2])
            result=c.fetchall()
            currentpenalty=float(result[0][0].replace("$",""))
            newpenaltyint=currentpenalty+0.5*(self.nowDate-returnDate).days
            newpenalty="$"+str(newpenaltyint)
            
            c.execute(SQL6,(newpenalty,self.data[0][2]))
            messagebox.showinfo("Notice","Charged for late return")


        db.commit()
        c.close()
        db.close()


    def penalty(self):

        self.penaltyScreen=Toplevel()
        self.penaltyScreen.title("Lost/Damaged Book")

        frame1=Frame(self.penaltyScreen)
        frame1.pack()
        frame2=Frame(self.penaltyScreen)
        frame2.pack()
        frame3=Frame(self.penaltyScreen)
        frame3.pack()

        self.svp1=StringVar()
        self.svp2=StringVar()
        self.svp3=StringVar()

        Label(frame1,text="ISBN").grid(row=0,column=0)
        Label(frame1,text="Current Time").grid(row=1,column=0)
        Label(frame1,text="Book Copy #").grid(row=0,column=2)
        Label(frame3,text="Last User of the Book").grid(row=0,column=0)
        Label(frame3,text="Amount to be charged").grid(row=1,column=0)

        self.entryp1=Entry(frame1)
        self.entryp1.grid(row=0,column=1)
        Entry(frame1,textvariable=self.svp1,state="readonly").grid(row=1,column=1)
        Entry(frame3,textvariable=self.svp3,state="readonly").grid(row=0,column=1)
        self.entryp2=Entry(frame3)
        self.entryp2.grid(row=1,column=1)

        now=datetime.datetime.now()
        nowdate=now.date()
        self.svp1.set(now)
        self.svp2.set("")
        OptionMenu(frame1, self.svp2,"1","2","3","4","5","6","7").grid(row=0,column=3)

        Button(frame2,text="Look for the last user",command=self.penaltyDB1).pack()
        Button(frame3,text="Submit",command=self.penaltyDB2).grid(row=2,column=2)
        Button(frame3,text="cancel",command=self.tt).grid(row=2,column=3)

    def tt(self):
        self.penaltyScreen.withdraw()
        self.menu2.deiconify()


    def penaltyDB1(self):


        db=self.Connect()
        c=db.cursor()

        try:

            SQL1="SELECT Cost, UserName,Is_Damaged, Is_Lost, Penalty FROM ISSUES_RECORD AS S NATURAL JOIN BOOK_COPY AS C NATURAL JOIN BOOK AS B NATURAL JOIN STUDENT_FACULTY AS F WHERE B.ISBN =%s AND C.Copy_Number=%s GROUP BY B.ISBN, C.Copy_Number ORDER BY S.Date_of_issue DESC LIMIT 1"
            c.execute(SQL1,(self.entryp1.get(),self.svp2.get()))
            data=c.fetchall()
            self.svp3.set(data[0][1])

        except:
            messagebox.showerror("Error", "Such copy number does not exist")
            self.svp3.set("")
            
            

 

        c.close()
        db.close()

    def penaltyDB2(self):

        db=self.Connect()
        c=db.cursor()
        try:
            SQL1="SELECT Cost, UserName,Is_Damaged, Is_Lost, Penalty FROM ISSUES_RECORD AS S NATURAL JOIN BOOK_COPY AS C NATURAL JOIN BOOK AS B NATURAL JOIN STUDENT_FACULTY AS F WHERE B.ISBN =%s AND C.Copy_Number=%s GROUP BY B.ISBN, C.Copy_Number ORDER BY S.Date_of_issue DESC LIMIT 1"
            c.execute(SQL1,(self.entryp1.get(),self.svp2.get()))
            info=c.fetchall()
            currentpenalty=info[0][4]
            penaltyint=int(currentpenalty.replace("$",""))
            newpenaltyint=penaltyint+int(self.entryp2.get().replace("$",""))
            newpenalty="$"+str(newpenaltyint)
            
            
            SQL2="UPDATE STUDENT_FACULTY SET Penalty=%s WHERE UserName=%s"
            c.execute(SQL2,(newpenalty,self.svp3.get()))

            if newpenaltyint>100:

                SQL3="UPDATE STUDENT_FACULTY SET Is_Debarred=%s WHERE UserName=%s"
                c.execute(SQL3,(1,self.svp3.get()))
            messagebox.showinfo("Notice", "Penalty charged")

            

        except:

            messagebox.showerror("Error", "Please find the last user and determine the amount to be charged")
            self.svp3.set("")

        db.commit()
        c.close()
        db.close()

    def damagedReport(self):
        
        self.w=Toplevel()
        self.w.title("Damaged Books Report")
        Label(self.w,text="Month",width=10).grid(row=0,column=0)
        
        self.entry31=StringVar()
        self.entry31.set("Select Month")
        OptionMenu(self.w,self.entry31,"January","Feburary","March").grid(row=0,column=1,stick=E+W)
        
        Label(self.w,text="Subject").grid(row=0,column=2)
        self.entry32=StringVar()
        self.entry32.set("Select Subject")
        OptionMenu(self.w, self.entry32,"Novel","Children","Technology","Lifestyle","Crazy","Georgraphy","Business").grid(row=0,column=3) 
        self.entry33=StringVar()
        Label(self.w,text="Subject",width=10).grid(row=1,column=2)
        self.entry33.set("Select Subject")
        OptionMenu(self.w,self.entry33,"Novel","Children","Technology","Lifestyle","Crazy","Georgraphy","Business").grid(row=1,column=3)
        Label(self.w,text="Subject").grid(row=2,column=2)
        self.entry34=StringVar()
        self.entry34.set("Select Subject")
        OptionMenu(self.w,self.entry34,"Novel","Children","Technology","Lifestyle","Crazy","Georgraphy","Business").grid(row=2,column=3)
        Button(self.w,text="Show report",command=self.showReport).grid(row=4,column=0,columnspan=4,sticky=E+W)
        Button(self.w,text="Back",command=self.ttt).grid(row=5,column=0,columnspan=4,sticky=E+W)
    def ttt(self):
        self.w.withdraw()
        self.menu2.deiconify()

        
    def showReport(self):
        month=self.entry31.get()
        subject1=self.entry32.get()
        subject2=self.entry33.get()
        subject3=self.entry34.get()

        monthInt=[]
        if self.entry31.get()=="January":
            monthInt=1
        elif self.entry31.get()=="Feburary":
            monthInt=2
        else:
            monthInt=3
        
        db=self.Connect()
        c=db.cursor()
        sql="""SELECT MONTH(Date_of_issue), Subject_Name, COUNT(Is_damaged)
               FROM BOOK_COPY, BOOK, ISSUES_RECORD
               WHERE BOOK_COPY.ISBN=ISSUES_RECORD.ISBN
               AND BOOK_COPY.Copy_Number=ISSUES_RECORD.Copy_Number
               AND BOOK_COPY.ISBN=BOOK.ISBN
               AND MONTH(Date_of_issue)=%s
               AND Subject_Name IN(%s,%s,%s)
               GROUP BY Subject_Name"""
        c.execute(sql,(monthInt,subject1,subject2,subject3))
        b=c.fetchall()

        

        if len(b)==0:
            messagebox.showinfo("Damaged Books Report","No damaged books!")
        else:
            f=Frame(self.w)
            f.grid(row=6,columnspan=4)
            Label(f,text="Month",width=20).grid(row=0,column=0)
            Label(f,text="Subject",width=20).grid(row=0,column=1)
            Label(f,text="#Damaged books",width=20).grid(row=0,column=2)
            if len(b)==1:
                Label(f,text=month).grid(row=1,column=0)
                Label(f,text=b[0][1]).grid(row=1,column=1)
                Label(f,text=b[0][2]).grid(row=1,column=2)
                Label(f,text=' ').grid(row=2,column=1)
                Label(f,text=' ').grid(row=2,column=2)
                Label(f,text=' ').grid(row=3,column=1)
                Label(f,text=' ').grid(row=3,column=2)
            elif len(b)==2:
                Label(f,text=month).grid(row=1,column=0)
                Label(f,text=b[0][1]).grid(row=1,column=1)
                Label(f,text=b[0][2]).grid(row=1,column=2)
                Label(f,text=b[1][1]).grid(row=2,column=1)
                Label(f,text=b[1][2]).grid(row=2,column=2)
                Label(f,text=' ').grid(row=3,column=1)
                Label(f,text=' ').grid(row=3,column=2)
            else:
                Label(f,text=month).grid(row=2,column=0)
                Label(f,text=subject1).grid(row=1,column=1)
                Label(f,text=b[0][2]).grid(row=1,column=2)
                Label(f,text=subject2).grid(row=2,column=1)
                Label(f,text=b[1][2]).grid(row=2,column=2)
                Label(f,text=subject3).grid(row=3,column=1)
                Label(f,text=b[2][2]).grid(row=3,column=2)
        
    def popSubjectReport(self):
        db=self.Connect()
        c=db.cursor()
        sql="""SELECT MONTH(S.Date_of_issue), B.Subject_Name, COUNT(S.Issue_ID)

               FROM ISSUES_RECORD AS S INNER JOIN BOOK_COPY AS C ON S.ISBN=C.ISBN
               AND
S.Copy_Number=C.Copy_Number INNER JOIN BOOK AS B on C.ISBN=B.ISBN

               WHERE MONTH(S.Date_of_issue) = 1 OR MONTH(S.Date_of_issue) = 2

               GROUP BY MONTH(S.Date_of_issue),B.Subject_Name
               ORDER BY COUNT(S.Issue_ID) DESC"""
        aDict={"Jan":[],"Feb":[]}
        c.execute(sql)
        b=c.fetchall()
        for item in b:
            if item[0]==1:
                aDict["Jan"].append((item[1],item[2]))
            else:
                aDict["Feb"].append((item[1],item[2]))


        self.popSubject=Toplevel()
        self.popSubject.title("Popular Subject Report")
        Label(self.popSubject,text="Month",width=10).grid(row=0,column=0)
        Label(self.popSubject,text="Top Subject",width=20).grid(row=0,column=1)
        Label(self.popSubject,text="#Checkouts",width=10).grid(row=0,column=2)

        Label(self.popSubject,text="Jan").grid(row=1,column=0)
        Label(self.popSubject,text=aDict["Jan"][0][0]).grid(row=1,column=1)
        Label(self.popSubject,text=aDict["Jan"][0][1]).grid(row=1,column=2)

        Label(self.popSubject,text="").grid(row=2,column=0)
        Label(self.popSubject,text=aDict["Jan"][1][0]).grid(row=2,column=1)
        Label(self.popSubject,text=aDict["Jan"][1][1]).grid(row=2,column=2)

        Label(self.popSubject,text="").grid(row=3,column=0)
        Label(self.popSubject,text=aDict["Jan"][2][0]).grid(row=3,column=1)
        Label(self.popSubject,text=aDict["Jan"][2][1]).grid(row=3,column=2)

        Label(self.popSubject,text="Feb").grid(row=4,column=0)
        Label(self.popSubject,text=aDict["Feb"][0][0]).grid(row=4,column=1)
        Label(self.popSubject,text=aDict["Feb"][0][1]).grid(row=4,column=2)

        Label(self.popSubject,text="").grid(row=5,column=0)
        Label(self.popSubject,text=aDict["Feb"][1][0]).grid(row=5,column=1)
        Label(self.popSubject,text=aDict["Feb"][1][1]).grid(row=5,column=2)

        Label(self.popSubject,text="").grid(row=6,column=0)
        Label(self.popSubject,text=aDict["Feb"][2][0]).grid(row=6,column=1)
        Label(self.popSubject,text=aDict["Feb"][2][1]).grid(row=6,column=2)

        Button(self.popSubject,text="Back",command=self.ttt2).grid(row=7,column=1,columnspan=2,sticky=EW)
        
    def ttt2(self):
        self.popSubject.withdraw()
        self.menu2.deiconify()


    def frequentUserReport(self):
        db=self.Connect()
        c=db.cursor()
        sql1="""SELECT MONTH(S.Date_of_issue), U.UserName, COUNT(S.Issue_ID) AS Count
               FROM ISSUES_RECORD AS S INNER JOIN USER AS U ON S.UserName=U.UserName

               WHERE MONTH(S.Date_of_issue) = 1
               GROUP BY MONTH(S.Date_of_issue), U.UserName
               HAVING
Count >= 2

               ORDER BY Count DESC
LIMIT 5"""
        sql2="""SELECT MONTH(S.Date_of_issue), U.UserName, COUNT(S.Issue_ID) AS Count
               FROM ISSUES_RECORD AS S INNER JOIN USER AS U ON S.UserName=U.UserName

               WHERE MONTH(S.Date_of_issue) = 2
               GROUP BY MONTH(S.Date_of_issue), U.UserName
               HAVING
Count >= 2

               ORDER BY Count DESC
LIMIT 5"""

        c.execute(sql1)
        b1=c.fetchall()
        aDict={"Jan":[],"Feb":[]}
        for item in b1:
            aDict["Jan"].append((item[1],item[2]))

        c.execute(sql2)
        b2=c.fetchall()
        for item in b2:
            aDict["Feb"].append((item[1],item[2]))
        
        
        

        self.frequentUser=Toplevel()
        self.frequentUser.title("Frequent Users Report")
        Label(self.frequentUser,text="Month",width=10).grid(row=0,column=0)
        Label(self.frequentUser,text="User Name",width=20).grid(row=0,column=1)
        Label(self.frequentUser,text="#Checkouts",width=10).grid(row=0,column=2)
        for item in aDict:
            if item=="Jan":
                Label(self.frequentUser,text="Jan",width=20).grid(row=1,column=0)
                for i in range(len(aDict["Jan"])):
                    print(i)
                    Label(self.frequentUser,text=aDict["Jan"][i][0]).grid(row=1+i,column=1)
                    Label(self.frequentUser,text=aDict["Jan"][i][1]).grid(row=1+i,column=2)
            else:
                Label(self.frequentUser,text="Feb",width=20).grid(row=5,column=0)
                for i in range(len(aDict["Feb"])):
                    Label(self.frequentUser,text=aDict["Feb"][i][0]).grid(row=5+i,column=1)
                    Label(self.frequentUser,text=aDict["Feb"][i][1]).grid(row=5+i,column=2)

        Button(self.frequentUser,text="Back",command=self.ttt3).grid(row=20,column=1,columnspan=2,sticky=EW)
        
    def ttt3(self):
        self.frequentUser.withdraw()
        self.menu2.deiconify()

                    
            
    def popBooksReport(self):
        db=self.Connect()
        c=db.cursor()
        sql1="""SELECT MONTH(S.Date_of_issue), Title, COUNT(S.Issue_ID)

                FROM ISSUES_RECORD AS S INNER JOIN BOOK_COPY AS C ON S.ISBN=C.ISBN
                AND
S.Copy_Number=C.Copy_Number INNER JOIN BOOK AS B on C.ISBN=B.ISBN

                WHERE MONTH(S.Date_of_issue)= 1
                GROUP BY MONTH(S.Date_of_issue), B.Title
                ORDER BY COUNT(S.Issue_ID) DESC LIMIT 3"""
        sql2="""SELECT MONTH(S.Date_of_issue), Title, COUNT(S.Issue_ID)

                FROM ISSUES_RECORD AS S INNER JOIN BOOK_COPY AS C ON S.ISBN=C.ISBN
                AND
S.Copy_Number=C.Copy_Number INNER JOIN BOOK AS B on C.ISBN=B.ISBN

                WHERE MONTH(S.Date_of_issue)=2

                GROUP BY MONTH(S.Date_of_issue), B.Title
                ORDER BY COUNT(S.Issue_ID) DESC LIMIT 3"""
        c.execute(sql1)
        b1=c.fetchall()
        aDict={"Jan":[],"Feb":[]}
        for item in b1:
            aDict['Jan'].append((item[1],item[2]))

        c.execute(sql2)
        b2=c.fetchall()
        for item in b2: 
            aDict['Feb'].append((item[1],item[2]))
        
       
        self.popBookReport=Toplevel()
        self.popBookReport.title("Popular Books Report")
        Label(self.popBookReport,text="Month",width=10).grid(row=0,column=0)
        Label(self.popBookReport,text="Title",width=20).grid(row=0,column=1)
        Label(self.popBookReport,text="#Checkouts").grid(row=0,column=2)

        Label(self.popBookReport,text='Jan',width=10).grid(row=1,column=0)
        Label(self.popBookReport,text=aDict['Jan'][0][0]).grid(row=1,column=1)
        Label(self.popBookReport,text=aDict['Jan'][0][1]).grid(row=1,column=2)

        Label(self.popBookReport,text='').grid(row=2,column=0)
        Label(self.popBookReport,text=aDict['Jan'][1][0]).grid(row=2,column=1)
        Label(self.popBookReport,text=aDict['Jan'][1][1]).grid(row=2,column=2)
        
        Label(self.popBookReport,text='').grid(row=3,column=0)
        Label(self.popBookReport,text=aDict['Jan'][2][0]).grid(row=3,column=1)
        Label(self.popBookReport,text=aDict['Jan'][2][1]).grid(row=3,column=2)

        Label(self.popBookReport,text='Feb').grid(row=4,column=0)
        Label(self.popBookReport,text=aDict['Feb'][0][0]).grid(row=4,column=1)
        Label(self.popBookReport,text=aDict['Feb'][0][1]).grid(row=4,column=2)

        Label(self.popBookReport,text='').grid(row=5,column=0)
        Label(self.popBookReport,text=aDict['Feb'][1][0]).grid(row=5,column=1)
        Label(self.popBookReport,text=aDict['Feb'][1][1]).grid(row=5,column=2)

        Label(self.popBookReport,text='').grid(row=6,column=0)
        Label(self.popBookReport,text=aDict['Feb'][2][0]).grid(row=6,column=1)
        Label(self.popBookReport,text=aDict['Feb'][2][1]).grid(row=6,column=2)

        Button(self.popBookReport,text="Back",command=self.ttt4).grid(row=10,column=1,columnspan=2,sticky=EW)
        
    def ttt4(self):
        self.popBookReport.withdraw()
        self.menu2.deiconify()




    



root=Tk()
App(root)
root.mainloop()
 

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from tkcalendar import DateEntry
class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        def int_validate(inp):
            if inp.isdigit():
                return True
            elif inp is "":
                return True
            else:
                return False

        # ------- All Variable -------
        self.Roll_No_var=StringVar()
        self.name_var=StringVar()
        self.dob_var=StringVar()
        self.doj_var=StringVar()

        # ------- Manage Frame -------
        Manage_Frame=Frame(self.root,bd=4,relief=RIDGE)
        Manage_Frame.place(x=20,y=100,width=500,height=560)

        m_title=Label(Manage_Frame,text="Please Fill Form",font=("times new roman",30,"bold"))
        m_title.grid(row=0,columnspan=2,pady=10)

        lbl_roll=Label(Manage_Frame,text="Roll No.",font=("times new roman",20,"bold"))
        lbl_roll.grid(row=1,column=0,pady=10,padx=20,sticky="w")

        self.txt_roll=Entry(Manage_Frame,textvariable=self.Roll_No_var,font=("times new roman",20,"bold"),bd=5,relief=GROOVE)
        self.txt_roll.grid(row=1,column=1,pady=10,padx=20,sticky="w")

        lbl_name=Label(Manage_Frame,text="Name",font=("times new roman",20,"bold"))
        lbl_name.grid(row=2,column=0,pady=10,padx=20,sticky="w")

        txt_name=Entry(Manage_Frame,textvariable=self.name_var,font=("times new roman",20,"bold"),bd=5,relief=GROOVE)
        txt_name.grid(row=2,column=1,pady=10,padx=20,sticky="w")

        lbl_dob=Label(Manage_Frame,text="DOB",font=("times new roman",20,"bold"))
        lbl_dob.grid(row=3,column=0,pady=10,padx=20,sticky="w")

        cal_dob=DateEntry(Manage_Frame,selectmode='day', date_pattern='yyyy-mm-dd',textvariable=self.dob_var,font=("times new roman",20,"bold"),bd=5,relief=GROOVE)
        cal_dob.grid(row=3,column=1,pady=10,padx=20,sticky="w")

        lbl_doj=Label(Manage_Frame,text="DOJ",font=("times new roman",20,"bold"))
        lbl_doj.grid(row=4,column=0,pady=10,padx=20,sticky="w")

        cal_doj=DateEntry(Manage_Frame,selectmode='day',date_pattern='yyyy-mm-dd',textvariable=self.doj_var,font=("times new roman",20,"bold"),bd=5,relief=GROOVE)
        cal_doj.grid(row=4,column=1,pady=10,padx=20,sticky="w")


        # ------- Button Frame -------
        btn_Frame=Frame(Manage_Frame,bd=4,relief=RIDGE)
        btn_Frame.place(x=15,y=500,width=460,height=50)

        Addbtn=Button(btn_Frame,text="Add",command=self.add_student_data,width=10).grid(row=0,column=0,padx=10,pady=10)
        updatebtn=Button(btn_Frame,text="Update",command=self.update_student,width=10).grid(row=0,column=1,padx=10,pady=10)
        deletebtn=Button(btn_Frame,text="Delete",command=self.delete_student,width=10).grid(row=0,column=2,padx=10,pady=10)
        Clearbtn=Button(btn_Frame,text="Clear",command=self.clear_student,width=10).grid(row=0,column=3,padx=10,pady=10)

        # ------- Detail Frame -------
        Detail_Frame=Frame(self.root,bd=4,relief=RIDGE)
        Detail_Frame.place(x=550,y=100,width=750,height=560)

     
        reg=root.register(int_validate)
        self.txt_roll.config(validate="key",validatecommand=(reg,'%P'))

        
        # ------- Table Frame --------
        Table_Frame=Frame(Detail_Frame,bd=4,relief=RIDGE)
        Table_Frame.place(x=20,y=70,width=700,height=470)

        scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)
        self.Student_Table=ttk.Treeview(Table_Frame,columns=("roll","name","dob","doj"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.Student_Table.xview)
        scroll_y.config(command=self.Student_Table.yview)
        self.Student_Table.heading("roll",text="Roll No.")
        self.Student_Table.heading("name",text="Name")
        self.Student_Table.heading("dob",text="DOB")
    
        self.Student_Table.heading("doj",text="DOJ")
        self.Student_Table['show']='headings'
        self.Student_Table.column("roll",width=100)
        self.Student_Table.column("name",width=130)
        self.Student_Table.column("dob",width=120)
     
        self.Student_Table.column("doj",width=100)
        self.Student_Table.pack(fill=BOTH,expand=1)
        self.Student_Table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()


    def add_student_data(self):
        con=mysql.connector.connect(host="localhost",user="root",password="root",database="student_db")
        cur=con.cursor()

        cur.execute("insert into student(student_no,student_name,student_dob,student_doj) values(%s,%s,%s,%s)",(self.Roll_No_var.get(),self.name_var.get(),self.dob_var.get(),self.doj_var.get() ))

        con.commit()
        self.fetch_data()
        self.clear_student()
        con.close()
        messagebox.showinfo("Information","Data Inserted")
        
    def fetch_data(self):
        con=mysql.connector.connect(host="localhost",user="pawan",password="root",database="student_db")
        cur=con.cursor()

        cur.execute("select * from student")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.Student_Table.delete(*self.Student_Table.get_children())
            for row in rows:
                self.Student_Table.insert('',END,values=row)
            con.commit()
        else:
            self.Student_Table.delete(*self.Student_Table.get_children())
            for row in rows:
                self.Student_Table.insert('',END,values=row)
            con.commit()
        con.close()



    def update_student(self):
        con=mysql.connector.connect(host="localhost",user="pawan",password="root",database="student_db")
        cur=con.cursor()
        cur.execute("update student set student_name=%s,student_dob=%s,student_doj=%s where student_no=%s",(self.name_var.get(),self.dob_var.get(),self.doj_var.get(),self.Roll_No_var.get() ))
        con.commit()
        self.fetch_data()
        self.clear_student()
        con.close()
        messagebox.showinfo("Information","Data Updated")
        

    def delete_student(self):

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='student_db',
                                                 user='pawan',
                                                 password='root')
            cursor = connection.cursor()
            sql_Delete_query = """Delete from student where student_no = %s"""
            laptopId = self.Roll_No_var.get()
            cursor.execute(sql_Delete_query, (laptopId,))
            #connection.commit()
            print("Record Deleted successfully ")
            connection.commit()
            connection.close()
            self.fetch_data()
            self.clear_student()

        except mysql.connector.Error as error:
            print("Failed to Delete record from table: {}".format(error))
                    

    def clear_student(self):
       self.Roll_No_var.set("")
       self.name_var.set("")
       self.dob_var.set("")
       self.doj_var.set("")
    

    def get_cursor(self,ev):
       cursor_row = self.Student_Table.focus()
       contents = self.Student_Table.item(cursor_row)
       row=contents['values']
       self.Roll_No_var.set(row[0])
       self.name_var.set(row[1])
       self.dob_var.set(row[2])
       self.doj_var.set(row[3])
       
    

root = Tk()
ob=Student(root)

root.mainloop()

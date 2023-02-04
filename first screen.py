import os
from tkinter import *
from tkinter import messagebox

#create a window
Window=Tk()
Window.geometry("1920x1080")
Window.title("MAIL OTP")

def verify():
    #sender mail id is stored in variable cmd
    cmd=str(email.get())
    #Construct and storing the command in string variable called temp
    temp='python sendmail.py'+' '+cmd
    #Call another program
    os.system(temp)

label1=Label(Window,text="One Time Password",relief="solid",font=("arial",26,"bold"),fg='blue').pack(fill=BOTH)
email=StringVar()
Re=Label(Window,text="EMAIL ID",font=("arial",22,"bold")).place(x=0,y=50)
w=Entry(Window,width=20,validate="key",textvariable=email)
w.place(x=900,y=50)
log = Button(Window, text="Proceed",relief="raised", bg='yellow', font=("arial", 26, "bold"), fg='black',command=verify).place(x=900,y=150)
Window.mainloop()
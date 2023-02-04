from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
root = Tk()
root.title("Python: Simple Inventory System")
 
width = 640
height = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
def Database():
    global conn, cursor
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, firstname TEXT, lastname TEXT)")

USERNAME = StringVar()
PASSWORD = StringVar()
OTP = StringVar()
NEW_PASS = StringVar()
RESET_PASS = StringVar()
def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.pack(side=TOP, pady=80)
    lbl_username = Label(LoginFrame, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)
    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=Login)
    btn_login.grid(row=4, columnspan=2, pady=20)
    lbl_register = Label(LoginFrame, text="Register", fg="Blue", font=('arial', 12))
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)
    lbl_register2 = Label(LoginFrame, text="Forget Password", fg="Blue", font=('arial', 12))
    lbl_register2.grid(row=5, columnspan=2, sticky=W)
    lbl_register2.bind('<Button-1>', ToggleToResetpass)


def ResetPass():
    global PassFrame, lbl_result3
    PassFrame = Frame(root)
    PassFrame.pack(side=TOP, pady=80)
    lbl_pass1 = Label(PassFrame, text="OTP:", font=('arial', 25), bd=18)
    lbl_pass1.grid(row=1)
    lbl_pass2 = Label(PassFrame, text="New Password:", font=('arial', 25), bd=18)
    lbl_pass2.grid(row=2)
    lbl_pass3 = Label(PassFrame, text="Retype Password:", font=('arial', 25), bd=18)
    lbl_pass3.grid(row=3)
    lbl_result3 = Button(PassFrame, text="", font=('arial', 18))
    lbl_result3.grid(row=3, columnspan=2)
    pass1 = Entry(PassFrame, font=('arial', 20), textvariable=OTP, width=15)
    pass1.grid(row=1, column=1)
    pass2 = Entry(PassFrame, font=('arial', 20), textvariable=NEW_PASS, width=15)
    pass2.grid(row=2, column=1)
    pass3 = Entry(PassFrame, font=('arial', 20), textvariable=RESET_PASS, width=15)
    pass3.grid(row=3, column=1)
    btn_reset = Button(PassFrame, text="Login", font=('arial', 18), width=35, command=Reset)
    btn_reset.grid(row=4, columnspan=2, pady=20)
    lbl_reset = Label(PassFrame, text="Reset", fg="Blue", font=('arial', 12))
    lbl_reset.grid(row=5, sticky=W)
    lbl_reset.bind('<Button-1>', ToggleToAfterReset)


def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()
 
def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()
 
def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()
    
def ToggleToResetpass(event=None):
    LoginFrame.destroy()
    ResetPass()

def ToggleToAfterReset(event=None):
    PassFrame.destroy()
    LoginForm()
    
def Login():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            lbl_result1.config(text="You Successfully Login", fg="blue")
        else:
            lbl_result1.config(text="Invalid Username or password", fg="red")
LoginForm()

def check(password):
    if(len(password)<=8):
        return 0;
    elif not re.search("[a-z]",NEW_PASS.get()):
        return 0
    elif not re.search("[A-Z]",NEW_PASS.get()):
        return 0
    elif not re.search("[0-9]",NEW_PASS.get()):
        return 0
    elif not res.search("[_@$]",NEW_PASS.get()):
        return 0
    elif re.search("\s",NEW_PASS.get()):
        return 0
    else:
        return 1;
            
        
def Reset():
    Database()
    if OTP.get() == "" or NEW_PASS.get() == "" or RESET_PASS.get() == "":
        lbl_result3.config(text="Please complete the required field!",fg="orange")
    elif not OTP.get()=="" and not NEW_PASS.get()=="" and not RESET_PASS.get()=="":
        while True:
            if check(NEW_PASS.get())==0:
                lbl_result3.config(text="invalid",fg="orange")
            elif check(NEW_PASS.get())==1 and NEW_PASS.get()==RESET_PASS.get():
                lbl_result3.config(text="valid",fg="orange")
                cursor.execute("UPDATE TABLE_NAME SET 'PASSWORD'=? WHERE 'USERNAME'=? ", (NEW_PASS.get(),USERNAME.get(),))
                lnl_result3.config(text="Successfully updated!",gf="black")
                break
            elif check(NEW_PASS.get())==1 and NEW_PASS.get()!=RESET_PASS.get():
                  lbl_result3.config(text="Password unmatched",fg="orange")     
                       
                       
    cursor.close()
    conn.close()
    
if __name__ == '__main__':
    root.mainloop()

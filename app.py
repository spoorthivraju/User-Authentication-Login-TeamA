import psycopg2
from flask import Flask, render_template, request, redirect, url_for, render_template, session, send_from_directory, send_file, flash, abort, make_response
import decimal
import itertools 
from otp import send_email, generateOtp

app = Flask(__name__)
#Can use this to connect it to our database
try:
    db = psycopg2.connect(database="team_a", user = "postgres", password="your_postgres_pswd")
except:
    print("not connected")
    exit()
cur = db.cursor()

@app.route('/home', methods=['POST', 'GET'])
def logout():
    return render_template("sample.html")

@app.route('/', methods=['GET'])
def register():
    if request.method == "GET":
        return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if request.method == "GET":
        email = session['email']
        send_email(email)
        return render_template("sample.html", msg="sent email to" + email)

@app.route('/after-otp', methods=['GET', 'POST'])
def after_otp():
    if request.method == "POST":
        email = session['email']
        otp = session['otp']
        entered_otp = request.form['otp']
        print(otp, entered_otp, type(entered_otp), type(otp))
        if (otp == entered_otp):
            return render_template("sample.html", msg="success")
        return render_template("sample.html", msg="sent email to" + email)



@app.route('/registerUser', methods = ['POST'])
def registerCustomer():
    if request.method == 'POST':
        cfname = request.form['cfname']
        clname = request.form['clname']
        cphone = request.form['cphone']
        cuname = request.form['cuname']
        cemail = request.form['cemail']
        cpassword = request.form['cpassword']
        #Find out ID
        cur.execute("SELECT COUNT(*) FROM USERS;")
        row = cur.fetchall()
        row1 = list(itertools.chain(*row))
        cid = row1[0] + 1
        print(cid, cfname)
        #session['id'] = cid
        cur.execute("SELECT phonenumber, email from USERS")
        cpe = cur.fetchall()
        c_ph = [''.join(i[0]) for i in cpe]
        c_mail = [''.join(i[1]) for i in cpe]
        print("reg customer", c_ph, c_mail, cphone, cemail)
        if cphone not in c_ph and cemail not in c_mail: 
            cur.execute("INSERT INTO USERS VALUES(%s, %s, %s, %s, %s, %s, %s);", (cid, cuname, cpassword, cfname, clname, cphone, cemail))
            db.commit()
            return render_template("login.html", msg="login to continue")
        else:
            return render_template("error.html", error="email/phone number already exists!")

@app.route('/after-login', methods=['POST'])
def after_login():
    if request.method == "POST":
        uname = request.form['cuname']
        pswd = request.form['cpassword']
        print(pswd, uname)
        #Customer Validation
        cur.execute("SELECT email, userid, pswd from USERS WHERE username = %s", (uname, ))
        row = cur.fetchall() #row = [('password')]
        row = list(itertools.chain(*row))
        print(row[2], pswd, type(row[0]), type(pswd))
        if row[2] == pswd:
                session['id'] = row[1]
                session['email'] = row[0]
                email = session['email']
                print(email)
                otp = generateOtp()
                session['otp'] = otp
                send_email(email, otp)
                return render_template("otp.html", msg="sent email to " + email)
                return redirect("/otp") #changed
        print("incorrect")
        return render_template("login.html", msg="Incorrect password!!")
        

if __name__ == "__main__":
    app.secret_key = 'secret'
    app.run(host='127.0.0.1', debug=True)

import psycopg2
from flask import Flask, render_template, request, redirect, url_for, render_template, session, send_from_directory, send_file, flash, abort, make_response, flash
import decimal
import itertools 
from otp import send_email, generateOtp
#from db import insert
from security_questions import questions, get_random_ques
from password import password_check
from number_verification import mobile_otp,check_mobile_otp


app = Flask(__name__)
#Can use this to connect it to our database
try:
    db = psycopg2.connect(database="team_a", user = "postgres", password="Kartik@800")
except:
    print("not connected")
    exit()
cur = db.cursor()


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == "GET":
            print("inside register")
            q = questions()
            return render_template("register.html", q=q)
        elif request.method == "POST":
            cfname = request.form['cfname']
            clname = request.form['clname']
            cphone = request.form['cphone']
            cuname = request.form['cuname']
            cemail = request.form['cemail']
            cpassword = request.form['cpassword']
            q1 = request.form['q1']
            q2 = request.form['q2']
            q3 = request.form['q3']
            q4 = request.form['q4']
            q5 = request.form['q5']
            hq1 = request.form['hq1']
            hq2 = request.form['hq2']
            hq3 = request.form['hq3']
            hq4 = request.form['hq4']
            hq5 = request.form['hq5']
            pswd_chk = password_check(cpassword)
            q = questions()
            #Find out ID
            cur.execute("SELECT COUNT(*) FROM USERS;")
            row = cur.fetchall()
            row1 = list(itertools.chain(*row))
            cid = row1[0] + 1
            #print(cid, cfname)
            cur.execute("SELECT phonenumber, email, username from USERS")
            cpeu = cur.fetchall()
            c_ph = [''.join(i[0]) for i in cpeu]
            c_mail = []
            if cemail != "":
                c_mail = [''.join(i[1]) for i in cpeu]
            c_user = [''.join(i[2]) for i in cpeu]
            #print("reg customer", c_ph, c_mail, cphone, cemail)
            if cphone not in c_ph and cemail not in c_mail and cuname not in c_user: 
                if pswd_chk != 1:
                    print(pswd_chk)
                    return render_template("register.html", error="Password not according to contraints", q=q)
                print("pswd check")
                cur.execute("INSERT INTO USERS VALUES(%s, %s, %s, %s, %s, %s, %s);", (cid, cuname, cpassword, cfname, clname, cphone, cemail))
                cur.execute("INSERT INTO QUESTIONS VALUES(%s, %s, %s, %s)", (cid, 1, q1, hq1))
                cur.execute("INSERT INTO QUESTIONS VALUES(%s, %s, %s, %s)", (cid, 2, q2, hq2))
                cur.execute("INSERT INTO QUESTIONS VALUES(%s, %s, %s, %s)", (cid, 3, q3, hq3))
                cur.execute("INSERT INTO QUESTIONS VALUES(%s, %s, %s, %s)", (cid, 4, q4, hq4))
                cur.execute("INSERT INTO QUESTIONS VALUES(%s, %s, %s, %s)", (cid, 5, q5, hq5))
                db.commit()
                session['id'] = cid
                return render_template("login.html", msg="login to continue")
            elif cphone in c_ph:
                return render_template("register.html", error = "phone number already exists!", q=q)
            elif cemail in c_mail:
                return render_template("register.html", error = "mail id already exists!",q=q)
            elif cuname in c_user:
                return render_template("register.html", error = "username already exists!", q=q)
            elif pswd_chk != 1:
                return render_template("register.html", error=pswd_chk, q=q)
            else:
                return render_template("error.html", error="email/phone number already exists!", q=q)
    except Exception as e:
        return render_template("error.html", error="Invalid access " + str(e))


@app.route('/', methods=['GET', 'POST'])
def login():
    try: 
        if request.method == "GET":
            return render_template("login.html")
    except Exception as e:
        return render_template("error.html", error="Invalid access " + str(e))

@app.route('/forgot_password', methods=['GET'])
def forgot_password():
        return render_template("forgot_password.html")
        

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    try:
        if request.method == "GET":
            email = session['email']
            send_email(email)
            return render_template("sample.html", msg="sent email to" + email)
        #elif request.method == "POST"
    except Exception as e:
        return render_template("error.html", error="Invalid access " + str(e))

# @app.route('/otp-mobile', methods=['GET', 'POST'])
# def otp():
#     try:
#         if request.method == "GET":
#             email = session['email']
#             send_email(email)
#             return render_template("sample.html", msg="sent email to" + email)
#         #elif request.method == "POST"
#     except Exception as e:
#         return render_template("error.html", error="Invalid access " + str(e))


@app.route('/send_otp', methods=['POST'])
def send_otp():
    if request.method == "POST":
        email = request.form['email']
        otp = generateOtp()
        session['otp']=otp
        send_email(email,otp)
        session['email'] = email
        return render_template("reset_pw_otp.html")


@app.route('/security-ques', methods=['GET', 'POST'])
def security_ques():
    try:
        if request.method == "GET":
            d = get_random_ques()
            d = list(d.items())
            session["d"] = d
            cur.execute("SELECT answer, hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], d[0][0]))
            row1 = cur.fetchall() #row = [('password')]
            row1 = list(itertools.chain(*row1))
            cur.execute("SELECT answer, hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], d[1][0]))
            row2 = cur.fetchall() #row = [('password')]
            row2 = list(itertools.chain(*row2))
            cur.execute("SELECT answer, hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], d[2][0]))
            row3 = cur.fetchall() #row = [('password')]
            row3 = list(itertools.chain(*row3))
            return render_template("security_ques.html", q = d, a=row1[1], b=row2[1], c=row3[1])
        elif request.method == "POST":
            q1 = request.form['q1']
            q2 = request.form['q2']
            q3 = request.form['q3']
            d = session["d"]
            cur.execute("SELECT answer, hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], d[0][0]))
            row1 = cur.fetchall() #row = [('password')]
            row1 = list(itertools.chain(*row1))
            cur.execute("SELECT answer, hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], d[1][0]))
            row2 = cur.fetchall() #row = [('password')]
            row2 = list(itertools.chain(*row2))
            cur.execute("SELECT answer, hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], d[2][0]))
            row3 = cur.fetchall() #row = [('password')]
            row3 = list(itertools.chain(*row3))
            print(q1, q2, q3, row1, row2, row3)
            if q1 == row1[0] and q2 == row2[0] and q3 == row3[0]:
                return render_template("sample2.html", msg="successful login")
            else:
                return render_template("security_ques.html", error="wrong answers", q = d, a=row1[1], b=row2[1], c=row3[1])
    except Exception as e:
        return render_template("error.html", error="Invalid access "+ str(e))



@app.route('/after-otp', methods=['GET', 'POST'])
def after_otp():
    try:
        if request.method == "POST":
            email = session['email']
            otp = session['otp']
            entered_otp = request.form['otp']
            print(otp, entered_otp, type(entered_otp), type(otp))
            if (otp == entered_otp):
                return redirect("/security-ques")
            return render_template("sample.html", msg="sent email to" + email)
    except Exception as e:
        return render_template("error.html", error="Invalid access " + str(e))
    
@app.route('/after-otp-mobile', methods=['GET', 'POST'])
def after_otp_mobile():
    try:
        if request.method == "POST":
            email = session['email']
            otp = session['otp']
            entered_otp = request.form['otp']
            print(otp, entered_otp, type(entered_otp), type(otp))
            if (check_mobile_otp(otp,entered_otp)=="approved"):
                return redirect("/security-ques")
            return render_template("sample.html", msg="sent email to" + email)
    except Exception as e:
        return render_template("error.html", error="Invalid access " + str(e))

@app.route('/reset-pw', methods=['GET', 'POST'])
def reset_pw():
         if request.method == "POST":
             otp_given = request.form['otp']
             if(otp_given==session['otp']):
                 return render_template("reset_pw.html")
         return render_template("sample.html")

@app.route('/check', methods=['POST'])
def check():
    new_password = request.form['new_password']
    print(new_password)
    confirm_password = request.form['confirm_password']
    print(confirm_password)
    email = session['email']
    print(session['email'])
    if(new_password == confirm_password):
        if not password_check(new_password):
            return render_template("reset_pw.html", msg="unsatisfying password")
        elif len(new_password. splitlines()) > 1:
            return render_template("reset_pw.html", msg="unsatisfying password")
        else:
            cur.execute("SELECT username from users where email='"+email+"'")
            row = cur.fetchall()
            row = list(itertools.chain(*row))
            if(len(row)==0):
                return render_template("login.html", msg="User doesnt exist")    
            cur.execute("UPDATE users SET pswd=%s where email=%s", (new_password, email))
            db.commit()
            flash("Password updated!")  
            return render_template("login.html", msg="Password updated")

    
    else:
        return render_template("reset_pw.html", msg="The passwords don't match")
    

@app.route('/after-login', methods=['POST'])
def after_login():
        if request.method == "POST":
            uname = request.form['cuname']
            pswd = request.form['cpassword']
            print(pswd, uname)
            #Customer Validation
            cur.execute("SELECT email, userid, pswd,phonenumber from USERS WHERE username = %s", (uname, ))
            row = cur.fetchall() #row = [('password')]
            row = list(itertools.chain(*row))
            print(row[2], pswd, type(row[0]), type(pswd))
            if row[2] == pswd:
                    session['id'] = row[1]
                    session['email'] = row[0]
                    email = session['email']
                    if(email != ""):
                        print(email)
                        otp = generateOtp()
                        session['otp'] = otp
                        send_email(email,otp)
                        return render_template("otp.html", msg="sent email to " + email)
                        return redirect("/otp") #changed
                    else:
                        print("here")
                        phoneno=row[3]
                        otp = generateOtp()
                        session['otp'] = phoneno
                        print("generated otp")
                        mobile_otp(phoneno)
                        return render_template("otp-mobile.html", msg="sent otp to " + phoneno)
                        return redirect("/otp") #changed
                    
            print("incorrect")
            return render_template("login.html", msg="Incorrect password!!")


@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return redirect("/")        

if __name__ == "__main__":
    app.secret_key = 'secret'
    app.run(host='127.0.0.1', debug=True)
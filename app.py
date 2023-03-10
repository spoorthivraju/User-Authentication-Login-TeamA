import psycopg2
import decimal
import itertools

from flask import Flask, render_template, request, redirect, url_for, render_template, session, send_from_directory, send_file, flash, abort, make_response, flash 
import bcrypt
from otp import send_email, generate_otp
from security_questions import get_questions, get_random_questions
from password import password_check
from number_verification import mobile_otp,check_mobile_otp
import json


fname = "config.json"

with open(fname) as f:
    appConf = json.load(f)
    
    
app = Flask(__name__)
'''
DB connection
'''
try:
    #db = psycopg2.connect(database="team_a", user = "postgres", password="your_pswd")
    db = psycopg2.connect(database= appConf['database_connection']['database'], user =appConf['database_connection']['user'], \
        password = appConf['database_connection']['password'])
except:
    print("not connected")
    exit()
cursor = db.cursor()

@app.route('/', methods=['GET'])
def login():
    '''
        renders the login page
    '''
    try: 
        if request.method == "GET":
            return render_template("login.html")
    except Exception as error:
        return render_template("error.html", error="Invalid access " + str(error))

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    GET request: renders the register page
    POST request: gets all the form data from register.html, uses count to get userid, checks if the username, email or phone already exist,
    inserts into users table and questions table
    '''
    try:

        if request.method == "GET":
            print("inside register")
            questions = get_questions()
            return render_template("register.html", questions = questions)

        elif request.method == "POST":

            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phone = request.form['phone']
            user_name = request.form['user_name']
            email = request.form['email']
            password = request.form['password']
            question1 = request.form['question1']
            question2 = request.form['question2']
            question3 = request.form['question3']
            question4 = request.form['question4']
            question5 = request.form['question5']
            hint1 = request.form['hint1']
            hint2 = request.form['hint2']
            hint3 = request.form['hint3']
            hint4 = request.form['hint4']
            hint5 = request.form['hint5']

            check_password = password_check(password)

            questions = get_questions()

            #Find out ID
            cursor.execute("SELECT COUNT(*) FROM USERS;")
            current_count = cursor.fetchall()
            print("check itertools content", current_count)
            current_count = list(itertools.chain(*current_count))
            print("check itertools content", current_count)
            user_id = current_count[0] + 1
            #print(cid, first_name)

            cursor.execute("SELECT phonenumber, email, username from USERS")
            phonenumber_email_username = cursor.fetchall()
            db_phonenumber = [''.join(row[0]) for row in phonenumber_email_username]
            db_username = [''.join(row[2]) for row in phonenumber_email_username]
            db_email = []
            if email != "":
                db_email = [''.join(row[1]) for row in phonenumber_email_username]
            #print("reg customer", c_ph, c_mail, phone, email)

            if phone not in db_phonenumber and email not in db_email and user_name not in db_username: 
                if check_password != 1:
                    return render_template("register.html", error="Password not according to contraints", questions=questions)
                password = password.encode('utf-8')
                encrypted_pass = bcrypt.hashpw(password, bcrypt.gensalt(10))
                encrypted_pass = encrypted_pass.decode('utf-8')
                cursor.execute("INSERT INTO USERS VALUES(%s, %s, %s, %s, %s, %s, %s);", (user_id, user_name, encrypted_pass, first_name, last_name, phone, email))
                #cursor.execute("INSERT INTO USERS VALUES(%s, %s, %s, %s, %s, %s, %s);", (user_id, user_name, password, first_name, last_name, phone, email))

                entered_answers_and_hints = ((user_id, 1, question1, hint1), (user_id, 2, question2, hint2), (user_id, 3, question3, hint3), \
                    (user_id, 4, question4, hint4), (user_id, 5, question5, hint5))
                cursor.executemany("INSERT INTO QUESTIONS (userid, qid, answer, hint) VALUES (%s, %s, %s, %s)", entered_answers_and_hints)
                db.commit()

                session['id'] = user_id

                return render_template("login.html", msg = "login to continue")

            elif phone in db_phonenumber:
                return render_template("register.html", error = "phone number already exists!", questions = questions)

            elif email in db_email:
                return render_template("register.html", error = "mail id already exists!",questions = questions)

            elif user_name in db_username:
                return render_template("register.html", error = "username already exists!", questions = questions)

            elif check_password != 1:
                return render_template("register.html", error = "Password not according to contraints", questions = questions)

            else:
                return render_template("error.html", error = "email/phone number already exists!", questions = questions)
    except Exception as error:
        return render_template("error.html", error="Invalid access " + str(error))

@app.route('/after-login', methods=['POST'])
def after_login():
    '''
    POST: fetches data from login.html, validates password, creates session cookies for id, email, if email is not null - send otp to mail else to phone
    '''
    try:
        if request.method == "POST":
            user_name = request.form['user_name']
            password = request.form['password']
            print(password, user_name)
            #Customer Validation
            cursor.execute("SELECT email, userid, pswd,phonenumber from USERS WHERE username = %s", (user_name, ))
            email_userid_password_phone = cursor.fetchall() #row = [('password')]
            email_userid_password_phone = list(itertools.chain(*email_userid_password_phone))
            print(email_userid_password_phone[2], password, type(email_userid_password_phone[0]), type(password))
            p=password.encode('utf-8')
            db_password = email_userid_password_phone[2]
            if bcrypt.checkpw(p, db_password.encode('utf-8')):
                    session['id'] = email_userid_password_phone[1]
                    session['email'] = email_userid_password_phone[0]
                    email = session['email']

                    if(email != "default"):
                        print(email)
                        otp = generate_otp()
                        session['otp'] = otp
                        send_email(email,otp)
                        return render_template("otp.html", msg="sent email to " + email)
                        return redirect("/otp") #changed

                    else:
                        print("here")
                        phone_number = email_userid_password_phone[3]
                        otp = generate_otp()
                        session['otp'] = phone_number
                        print("generated otp")
                        mobile_otp(phone_number)
                        return render_template("otp-mobile.html", msg="sent otp to " + phone_number)
                        return redirect("/otp") #changed
                    
            print("incorrect")
            return render_template("login.html", msg="Incorrect password!!")
    except Exception as error:
        return render_template("error.html", error="Invalid access " + str(error))


@app.route('/forgot_password', methods=['GET'])
def forgot_password():
        return render_template("forgot_password.html")
        

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    '''
    GET: sends OTP to mail
    '''
    try:
        if request.method == "GET":
            email = session['email']
            send_email(email)
            return render_template("sample.html", msg="sent email to" + email)
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
        print(email)
        cursor.execute("SELECT email FROM users WHERE email='{0}'".format(email))
        db_email = cursor.fetchall()
        if(db_email):
            session['reset_email'] = email
            otp = generate_otp()
            session['reset_otp'] = otp
            send_email(email,otp)
            return render_template("reset_pw_otp.html")
        else:
            return render_template("forgot_password.html", msg='Email not registered.')

@app.route('/after-otp', methods=['GET', 'POST'])
def after_otp():
    '''
    If the entered otp matches the otp cookie(sent to email), user gets redirected to security questions
    '''
    try:

        if request.method == "POST":
            email = session['email']
            otp = session['otp']
            entered_otp = request.form['otp']
            print(otp, entered_otp, type(entered_otp), type(otp))

            if (otp == entered_otp):
                return redirect("/security-ques")
            return render_template("otp.html", msg="wrong otp")

    except Exception as e:
        return render_template("error.html", error="Invalid access " + str(e))


@app.route('/security-ques', methods=['GET', 'POST'])
def security_ques():
    '''
        GET: it fetches random questions and the hint to display it to the user
        POST: fetches user entered answers from security_ques.html, uses random_questions to get answers from the db for validation 
    '''
    try:

        if request.method == "GET":
            random_questions = get_random_questions()
            random_questions = list(random_questions.items())
            session["random_questions"] = random_questions
            print("random ques", random_questions)

            cursor.execute("SELECT hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], random_questions[0][0]))
            hint1 = cursor.fetchall() #row = [('password')]
            hint1 = list(itertools.chain(*hint1))
            cursor.execute("SELECT hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], random_questions[1][0]))
            hint2 = cursor.fetchall() #row = [('password')]
            hint2 = list(itertools.chain(*hint2))
            cursor.execute("SELECT hint from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], random_questions[2][0]))
            hint3 = cursor.fetchall() #row = [('password')]
            hint3 = list(itertools.chain(*hint3))

            return render_template("security_ques.html", q = random_questions, a=hint1[0], b=hint2[0], c=hint3[0])

        elif request.method == "POST":
            answer1 = request.form['question1']
            answer2 = request.form['question2']
            answer3 = request.form['question3']
            random_questions = session["random_questions"]
            print("random ques", random_questions)
            cursor.execute("SELECT answer from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], random_questions[0][0]))
            db_answer1 = cursor.fetchall() #row = [('password')]
            db_answer1 = list(itertools.chain(*db_answer1))
            cursor.execute("SELECT answer from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], random_questions[1][0]))
            db_answer2 = cursor.fetchall() #row = [('password')]
            db_answer2 = list(itertools.chain(*db_answer2))
            cursor.execute("SELECT answer from QUESTIONS WHERE userid = %s and qid=%s", (session['id'], random_questions[2][0]))
            db_answer3 = cursor.fetchall() #row = [('password')]
            db_answer3 = list(itertools.chain(*db_answer3))
            print(answer1, answer2, answer3, db_answer1, db_answer2, db_answer3)

            if answer1 == db_answer1[0] and answer2 == db_answer2[0] and answer3 == db_answer3[0]:
                return render_template("sample2.html", msg="successful login")

            else:
                return render_template("security_ques.html", error="wrong answers", q = random_questions, a=db_answer1[1], b=db_answer2[1], c=db_answer3[1])

    except Exception as error:
        return render_template("error.html", error="Invalid access "+ str(error))
    
@app.route('/after-otp-mobile', methods=['GET', 'POST'])
def after_otp_mobile():
    '''
    If the entered otp matches the otp cookie(sent to phone), user gets redirected to security questions
    '''
    try:

        if request.method == "POST":
            email = session['email']
            otp = session['otp']
            entered_otp = request.form['otp']
            print(otp, entered_otp, type(entered_otp), type(otp))

            if (check_mobile_otp(otp,entered_otp)=="approved"):
                return redirect("/security-ques")
            return render_template("sample.html", error = "Didnt get through", msg="sent email to" + email)

    except Exception as e:
        return render_template("error.html", error="Invalid access " + str(e))

@app.route('/reset-pw', methods=['GET', 'POST'])
def reset_pw():
    '''
    If the entered otp matches, renders the reset password page
    '''
    if request.method == "POST":
        otp_given = request.form['otp']

    if (otp_given == session['reset_otp']):
        return render_template("reset_pw.html")

    return render_template("sample.html")

@app.route('/check', methods=['POST'])
def check():
    '''
    Validates the newly entered otp, checks if the user exists or not
    '''
    new_password = request.form['new_password']
    print(new_password)
    confirm_password = request.form['confirm_password']
    print(confirm_password)
    email = session['reset_email']
    print(session['reset_email'])

    if (new_password == confirm_password):

        if not password_check(new_password):
            return render_template("reset_pw.html", msg="unsatisfying password")

        else:   
            new_password = new_password.encode('utf-8')
            encrypted_pass = bcrypt.hashpw(new_password, bcrypt.gensalt(10))
            encrypted_pass = encrypted_pass.decode('utf-8')
            cursor.execute("UPDATE users SET pswd=%s where email=%s", (encrypted_pass, email))
            db.commit()
            flash("Password updated!")  
            session.clear()
            return render_template("login.html", msg="Password updated")

    
    else:
        return render_template("reset_pw.html", msg="The passwords don't match")
    
@app.route('/deboard', methods=['GET', 'POST'])
def deboard():
    if request.method == 'GET':
        return render_template("deboard.html")
    else:
        if request.method == "POST":

            email = session['deboard_email']
            otp = session['deboard_otp']
            entered_otp = request.form['otp']
            print(otp, entered_otp, type(entered_otp), type(otp))

            if (otp == entered_otp):
                #email
                cursor.execute("SELECT userid FROM users WHERE email='{0}'".format(email))
                #cursor.execute("SELECT userid from USERS where email=%s", (email))  
                user_id = cursor.fetchall()
                print("check userid", user_id)
                if user_id == None:
                    return render_template("sample.html", error="user doesn't exist")
                user_id = list(itertools.chain(*user_id))
                cursor.execute("DELETE FROM QUESTIONS where userid=%s", (user_id))
                cursor.execute("DELETE FROM users where userid=%s", (user_id))
                db.commit()
                return render_template("sample.html", msg="deboarded successfully")
            return render_template("sample.html", msg="Entered otp is wrong")

@app.route('/send_otp_deboard', methods=['POST'])
def send_otp_deboard():
    if request.method == "POST":
        email = request.form['email']
        print(email)
        cursor.execute("SELECT email FROM users WHERE email='{0}'".format(email))
        db_email = cursor.fetchall()
        print(db_email)
        if(db_email):
            session['deboard_email'] = email
            otp = generate_otp()
            session['deboard_otp'] = otp
            send_email(email,otp)
            return render_template("deboard_otp.html")
        else:
            return render_template("sample.html", msg='Email not registered.')

@app.route('/logout', methods=["GET"])
def logout():
    '''
    Clears all the cookies
    '''
    session.clear()
    return redirect("/")        

if __name__ == "__main__":
    app.secret_key = 'secret'
    app.run(host='127.0.0.1', debug=True)
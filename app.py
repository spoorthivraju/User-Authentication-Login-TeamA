import psycopg2
from flask import Flask, render_template, request, redirect, url_for, render_template, session, send_from_directory, send_file, flash, abort, make_response
import decimal
import itertools 
app = Flask(__name__)
#Can use this to connect it to our database
try:
    db = psycopg2.connect(database="team_a", user = "postgres", password="your_postgres_pswd")
except:
    print("not connected")
    exit()
cur = db.cursor()
#cur.execute("SELECT name FROM  where id=1;")
#cust_name = cur.fetchall()
#print("here", cust_name)
#print()

@app.route('/home', methods=['POST', 'GET'])
def logout():
    return render_template("sample.html")
@app.route('/register', methods=['GET'])
def register():
    if request.method == "GET":
        return render_template("register.html")
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
            #Create Cart for Customer
            #cur.execute("INSERT INTO CART VALUES(%s, %s);", (cid, cid))
            #db.commit()
            #After Registration move to homepage
            return redirect('/home')
        else:
            return render_template("error.html", error="email/phone number already exists!")

if __name__ == "__main__":
    app.secret_key = 'secret'
    app.run(host='127.0.0.1', debug=True)

import math
import random
import smtplib
from email.message import EmailMessage
import json
fname = "config.json"

with open(fname) as f:
    appConf = json.load(f)
    
#function to generate the otp
def generate_otp():
    #generating otp
    digits="0123456789"
    OTP=""
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    otp = OTP + " is your OTP"
    return OTP

def send_email(sender_email, otp):
    msg = EmailMessage()
    #otp = generate_otp()
    msg.set_content(otp)

    #asking user email
    #emailid = input("Enter your email: ")


    #adding message to the mail
    msg['Subject'] = 'OTP for Login'
    msg['From'] = "dinsja02@gmail.com"
    msg['To'] = sender_email

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(appConf['email_auth_cred']['senders_mail'],\
        appConf['email_auth_cred']['sender_mail_pswd'])
    server.send_message(msg)
    server.quit()



'''a = input("Enter Your OTP >>: ")

#verification of otp
if a == otp:
    print("Verified")
else:
    print("Please Check your OTP again")
    print(a)
    print(otp)'''

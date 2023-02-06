import math
import random
import smtplib
import json
from email.message import EmailMessage

#function to generate the otp
def generate_otp():
    #generating otp
    digits="0123456789"
    OTP=""
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    otp = OTP + " is your OTP"
    return OTP

def send_email(receiver_email, otp):
    msg = EmailMessage()
    #otp = generate_otp()
    msg.set_content(otp)

    #getting credentials from the json

    f = open('config.json')
    # returns JSON object as a dictionary
    data = json.load(f)
    email_sender_data = data['email_auth_cred']
    
    #extracting credentials
    senders_mail = email_sender_data['senders_mail']
    sender_mail_pswd =email_sender_data['sender_mail_pswd']


    #adding message to the mail
    msg['Subject'] = 'OTP for Login'
    msg['From'] = senders_mail
    msg['To'] = receiver_email

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(senders_mail, sender_mail_pswd)
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
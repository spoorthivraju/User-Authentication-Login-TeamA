import os,math
import random,sys
import smtplib
import time
import  os
from email.message import EmailMessage


#function to generate the otp
def generateOtp():
    #generating otp
    digits="0123456789"
    OTP=""
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    otp = OTP + " is your OTP"
    return OTP



def mailgenerate():
    msg = EmailMessage()
    otp = generateOtp()
    msg.set_content(otp)

#asking user email
    
    emailid = input("Enter your email: ")

#adding message to the mail
    msg['Subject'] = 'OTP for Login'
    msg['From'] = "dinsja02@gmail.com"
    msg['To'] = emailid

# Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("dinsja02@gmail.com", "pbcyatsbssfjjavn")
    server.send_message(msg)
    server.quit()
    count=3
    while(count):
        starttime=time.time()
        a = input("Enter Your OTP >>: ")
        endtime=time.time()
        tm=endtime-starttime
    #verification of otp
        if a == otp and tm<120 and count>0:
            print("Verified")
            return True
        elif a!=otp and tm<120 and count>0:
            print("Please Check your OTP again")
            count=count-1
            if count==0:
                mailgenerate()
            
        elif tm>120 or count==0:
            print("timer expired")
            mailgenerate()
    return True

mailgenerate()
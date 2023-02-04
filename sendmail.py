import os,math
import random,sys
import smtplib

#Collect the user entered mail id from previous program
mailid=sys.argv[1]

# sending otp to your gmail
digits="0123456789"
OTP=""
for i in range(6):
    OTP+=digits[math.floor(random.random()*10)]
msg='Your OTP Verification for app is '+OTP+' Note..  Please enter otp within 2 minutes and 3 attempts, otherwise it becomes invalid'

#store it on text file
file2=open("otp.txt","w")
file2.write(OTP)
file2.close()

# &&&&&&&&&&&&- sender mail id
# ************- Your app password.
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
#sender mail id and app password
s.login("dinsja02@gmail.com", "pbcyatsbssfjjavn")
print(msg)
s.sendmail('&&&&&&&&&&&',mailid,msg)

#call next program
os.system('python second.py')
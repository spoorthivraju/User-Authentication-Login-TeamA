special_char = '!@#$&*()^%'
def password_check(pswd):
    uppercase = 0
    lowercase = 0
    digit = 0
    specialchar = 0
    if len(pswd) < 8:
        return 0
    for i in pswd:
        if (i.isupper()):
            uppercase += 1
        elif (i.islower()):
            lowercase += 1
        elif (i.isdigit()):
            digit += 1
        elif i in special_char:
            specialchar += 1
    if uppercase < 1 or specialchar < 1 or lowercase < 1 or digit < 1:
        return 0
    else:
        return 1
        



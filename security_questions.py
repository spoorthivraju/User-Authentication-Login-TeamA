# Define a list of security questions and answers
import random
que=['1.What is your mother\'s maiden name?','2.What was the name of your first pet?\n','3.What is your favorite color?\n',
'4.Where was your best family vacation as a kid?\n','5.When you were young, what did you want to be when you grew up?\n']
security_questions =  {1: 'What is your mother\'s maiden name?', 2: 'What was the name of your first pet?', \
    3: 'What is your favorite color?', 4:  'Where was your best family vacation as a kid?', 5:  'When you were young, what did you want to be when you grew up?'}


def questions():
    return que
# Function to verify the answer to a security question
def verify_answer(question, answer):
    for item in security_questions:
        if item['question'] == question and item['answer'] == answer:
            return True
    return False

def get_random_ques():
    random_ques = random.sample(range(1, 6), 3)
    d = {}
    for i in random_ques:
        d[i] = security_questions[i]
    return d


# Main function to implement two-factor authentication
def two_factor_auth(username, password):
    # Verify username and password
    if username == 'user123' and password == 'pass123':
        # Prompt user to answer a security question
        print('Login Successful')
        for i in range(0,3):
            l=[]
            r=random.choice(security_questions)
            if r not in l:
                print('Hint for the below Question is ',r['hint'])
                answer = input(r["question"])
                if verify_answer(r['question'], answer):
                    print('Access granted!')
                    l.append(r)
                else:
                    print('Wrong Answer!..Access denied!')
                    return
            else:
                i-=1
    else:
        print('Wrong Credentials!..Access denied!')


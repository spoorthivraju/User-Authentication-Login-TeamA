# Define a list of security questions and answers
import random

security_questions =  {1: 'What is your mother\'s maiden name?', 2: 'What was the name of your first pet?', \
    3: 'What is your favorite color?', 4:  'Where was your best family vacation as a kid?', 5:  'When you were young, what did you want to be when you grew up?'}


def get_questions():
    return security_questions.values()

def get_random_questions():
    random_ques = random.sample(range(1, 6), 3)
    d = {}
    for i in random_ques:
        d[i] = security_questions[i]
    return d



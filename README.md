# Login-teamname

## Tasks
- [X] User authentication system - onboarding(name, email, password)
- [X] Security questions( 3 ques, hints, ans from any 5 random) 
- [X] Actual Login(3 factor login-username, password) 
- [X] OTP Module(send email with OTP)
- [X] Verification of security questions(flash any three random question, the ans should match the prev one)
- [X] Integration of all modules 
- [X] Database schema 
- [X] Additional module(forgot password, mobile otp) 

## Changes
- [X] Change variable names
- [X] Use multi row insert query
- [ ] Password Encryption
- [X] Config file
- [ ] Create a table for security questions
- [X] De-board 
- [ ] Add comments
- [ ] Figure out how to fix default and unique constraint on email

# Login-teamname

To run the Flask app:
python3 app.py
Open I used 127.0.0.1:5000/ to open the page, we can create more html pages and render them accordingly

To create the db:
open the psql shell and type:
\i  '/Users/path_to_file/create.sql'
## Schema
<img width="568" alt="schema" src="https://user-images.githubusercontent.com/73352576/216787399-566ede2e-d027-4927-bbc2-a2556ab6c3ac.png">
<img width="755" alt="users_schema" src="https://user-images.githubusercontent.com/73352576/217020210-412655e3-ed59-4d68-9584-a2b3bd55691d.png">


## Database content

<img width="568" alt="db-contents" src="https://user-images.githubusercontent.com/73352576/216804970-4eb05ab5-bf26-4012-a90b-f913cc9d6c08.png">


